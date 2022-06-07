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

func (rdb *RethinkDB) GetProjects(ctx context.Context, in *proto.GetProjectsInput) (*proto.GetProjectsOutput, error) {
	table := rdb.config.Database.Tables["projects"].Name

	c, e := r.Table(table).GetAllByIndex("email", in.Email).OrderBy(r.Desc("index")).Run(rdb.session)
	if e != nil {
		return new(proto.GetProjectsOutput), e
	}

	if c.IsNil() {
		return new(proto.GetProjectsOutput), grpc.Errorf(codes.NotFound, fmt.Sprintf("no projects found for '%s'", in.Email))
	}

	projects := []*proto.Project{}

	e = c.All(&projects)
	if e != nil {
		return new(proto.GetProjectsOutput), grpc.Errorf(codes.Internal, e.Error())
	}

	return &proto.GetProjectsOutput{Projects: projects}, nil
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
