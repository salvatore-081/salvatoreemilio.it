package rethinkDB

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/golang/protobuf/ptypes/empty"
	"github.com/salvatore.081/salvatoreemilio-it/proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	r "gopkg.in/rethinkdb/rethinkdb-go.v6"
)

func (rdb *RethinkDB) AddProject(ctx context.Context, in *proto.AddProjectInput) (*proto.Project, error) {
	table := rdb.config.Database.Tables["projects"].Name

	c, e := r.Table(table).GetAllByIndex("email", in.Email).Max("index").Pluck("index").Values().Default(0).Run(rdb.session)
	if e != nil {
		return new(proto.Project), grpc.Errorf(codes.Internal, e.Error())
	}

	results := []int32{}

	e = c.All(&results)
	if e != nil {
		return new(proto.Project), grpc.Errorf(codes.Internal, e.Error())
	}

	index := results[0] + 1

	wr, e := r.Table(table).Insert(proto.Project{
		Email:       in.Email,
		Title:       in.Title,
		Description: in.Description,
		Image:       in.Image,
		Tags:        in.Tags,
		Links:       in.Links,
		Index:       index,
	}, r.InsertOpts{
		ReturnChanges: true,
	}).RunWrite(rdb.session)
	if e != nil {
		return new(proto.Project), grpc.Errorf(codes.Internal, e.Error())
	}

	if len(wr.Changes) == 0 {
		return new(proto.Project), grpc.Errorf(codes.Internal, "unable to read the inserted resource")
	}

	d, e := json.Marshal(wr.Changes[0].NewValue)
	if e != nil {
		return new(proto.Project), grpc.Errorf(codes.Internal, e.Error())
	}

	p := proto.Project{}

	e = json.Unmarshal(d, &p)
	if e != nil {
		return new(proto.Project), grpc.Errorf(codes.Internal, e.Error())
	}

	return &p, nil
}

func (rdb *RethinkDB) GetProject(ctx context.Context, in *proto.GetProjectInput) (*proto.Project, error) {
	table := rdb.config.Database.Tables["projects"].Name

	c, e := r.Table(table).Get(in.Id).Run(rdb.session)
	if e != nil {
		return new(proto.Project), grpc.Errorf(codes.Internal, e.Error())
	}

	if c.IsNil() {
		return new(proto.Project), grpc.Errorf(codes.NotFound, fmt.Sprintf("no project found with id '%s'", in.Id))
	}

	projects := []*proto.Project{}

	e = c.All(&projects)
	if e != nil {
		return new(proto.Project), grpc.Errorf(codes.Internal, e.Error())
	}

	return projects[0], nil
}

func (rdb *RethinkDB) GetProjects(ctx context.Context, in *proto.GetProjectsInput) (*proto.GetProjectsOutput, error) {
	table := rdb.config.Database.Tables["projects"].Name

	c, e := r.Table(table).GetAllByIndex("email", in.Email).OrderBy(r.Desc("index")).Run(rdb.session)
	if e != nil {
		return new(proto.GetProjectsOutput), grpc.Errorf(codes.Internal, e.Error())
	}

	projects := []*proto.Project{}

	e = c.All(&projects)
	if e != nil {
		return new(proto.GetProjectsOutput), grpc.Errorf(codes.Internal, e.Error())
	}

	if len(projects) == 0 {
		return new(proto.GetProjectsOutput), grpc.Errorf(codes.NotFound, fmt.Sprintf("no projects found for '%s'", in.Email))
	}

	return &proto.GetProjectsOutput{Projects: projects}, nil
}

func (rdb *RethinkDB) UpdateProject(ctx context.Context, in *proto.UpdateProjectInput) (*proto.Project, error) {
	table := rdb.config.Database.Tables["projects"].Name

	if in == nil || len(in.Id) < 1 {
		return new(proto.Project), grpc.Errorf(codes.InvalidArgument, "'id' is missing")
	}

	if in.UpdateProjectInputPayload == nil || in.UpdateProjectInputPayload.Index == 0 && len(in.UpdateProjectInputPayload.Title) < 1 && (len(in.UpdateProjectInputPayload.Description) < 1 && len(in.UpdateProjectInputPayload.Image) < 1 && len(in.UpdateProjectInputPayload.Tags) < 1 && len(in.UpdateProjectInputPayload.Links) < 1) {
		return new(proto.Project), grpc.Errorf(codes.InvalidArgument, "UpdateProjectInputPayload payload cannot be empty")
	}

	wr, e := r.Table(table).Get(in.Id).Update(in.UpdateProjectInputPayload, r.UpdateOpts{
		ReturnChanges: "always",
	}).RunWrite(rdb.session)
	if e != nil {
		return new(proto.Project), grpc.Errorf(codes.Internal, e.Error())
	}

	project := proto.Project{}

	if wr.Skipped > 0 {
		return new(proto.Project), grpc.Errorf(codes.NotFound, fmt.Sprintf("no project found with id '%s'", in.Id))
	}

	d, e := json.Marshal(wr.Changes[0].NewValue)
	if e != nil {
		return new(proto.Project), grpc.Errorf(codes.Internal, e.Error())
	}

	e = json.Unmarshal(d, &project)
	if e != nil {
		return new(proto.Project), grpc.Errorf(codes.Internal, e.Error())
	}

	// TODO
	// the following codition could be implemented inside the first Rethink query
	// I will do it leter (maybe)
	if in.UpdateProjectInputPayload.Index != 0 {
		d, e = json.Marshal(wr.Changes[0].OldValue)
		if e != nil {
			return &project, grpc.Errorf(codes.Internal, e.Error())
		}

		old := proto.Project{}

		e = json.Unmarshal(d, &old)
		if e != nil {
			return &project, grpc.Errorf(codes.Internal, e.Error())
		}

		if old.Index != project.Index {
			_, e := r.Table(table).GetAllByIndex("email", project.Email).Filter(func(row r.Term) interface{} {
				return r.Branch(
					r.Expr(project.Index).Ge(r.Expr(old.Index)),
					row.Field("id").Ne(project.Id).And(row.Field("index").Ge(old.Index).And(row.Field("index").Le(project.Index))),
					row.Field("id").Ne(project.Id).And(row.Field("index").Ge(project.Index).And(row.Field("index").Le(old.Index))),
				)
			}).Update(func(row r.Term) interface{} {
				return r.Branch(
					r.Expr(project.Index).Ge(r.Expr(old.Index)),
					r.Object("index", row.Field("index").Sub(1)),
					r.Object("index", row.Field("index").Add(1)),
				)
			}).Run(rdb.session)
			if e != nil {
				return &project, e
			}
		}

		if e != nil {
			return &project, e
		}
	}

	return &project, nil
}

func (rdb *RethinkDB) DeleteProject(ctx context.Context, in *proto.DeleteProjectInput) (*empty.Empty, error) {
	table := rdb.config.Database.Tables["projects"].Name

	wr, e := r.Table(table).Get(in.Id).Delete(r.DeleteOpts{
		ReturnChanges: true,
	}).RunWrite(rdb.session)
	if e != nil {
		return new(empty.Empty), e
	}

	if len(wr.FirstError) > 0 {
		return new(empty.Empty), grpc.Errorf(codes.Internal, wr.FirstError)
	}

	if wr.Deleted < 1 {
		return new(empty.Empty), grpc.Errorf(codes.NotFound, fmt.Sprintf("no project found with id '%s'", in.Id))
	}

	return new(empty.Empty), nil
}

func (rdb *RethinkDB) WatchProjects(ctx context.Context, in *proto.WatchProjectsInput) (<-chan *proto.ProjectFeed, chan error) {
	table := rdb.config.Database.Tables["projects"].Name

	ch := make(chan *proto.ProjectFeed)
	e := make(chan error, 1)

	if in == nil || len(in.Email) < 1 {
		e <- grpc.Errorf(codes.InvalidArgument, "argument 'email' is required")
	} else {
		c, err := r.Table(table).GetAllByIndex("email", in.Email).Changes(r.ChangesOpts{
			IncludeInitial: true,
		}).Run(rdb.session)
		if err != nil {
			e <- grpc.Errorf(codes.Internal, err.Error())
		} else {
			go func(ctx context.Context) {
				<-ctx.Done()
				c.Close()
			}(ctx)

			go func() {
				if c.IsNil() {
					ctx.Done()
					e <- grpc.Errorf(codes.NotFound, fmt.Sprintf("no projects found with email '%s'", in.Email))
				}
				feed := proto.ProjectFeed{}
				for c.Next(&feed) {
					ch <- &feed
				}
			}()
		}
	}

	return ch, e
}
