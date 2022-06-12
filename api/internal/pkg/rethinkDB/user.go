package rethinkDB

import (
	"context"
	"encoding/json"
	"fmt"
	"strings"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	r "gopkg.in/rethinkdb/rethinkdb-go.v6"

	"github.com/salvatore.081/salvatoreemilio-it/models"
	"github.com/salvatore.081/salvatoreemilio-it/proto"
)

func (rdb *RethinkDB) AddUser(ctx context.Context, in *proto.AddUserInput) (*proto.User, error) {
	table := rdb.config.Database.Tables["users"].Name

	if in == nil || len(in.Email) < 1 {
		return new(proto.User), grpc.Errorf(codes.InvalidArgument, "'email' is missing")
	}

	wr, e := r.Table(table).Insert(in, r.InsertOpts{
		ReturnChanges: true,
	}).RunWrite(rdb.session)
	if e != nil {
		if strings.HasPrefix(e.Error(), "Duplicate primary key") {
			return new(proto.User), grpc.Errorf(codes.AlreadyExists, fmt.Sprintf("an user with email '%s' already exists", in.Email))
		}
		return new(proto.User), grpc.Errorf(codes.Internal, e.Error())
	}

	if len(wr.Changes) == 0 {
		return new(proto.User), grpc.Errorf(codes.Internal, "unable to read the inserted resource")
	}

	d, e := json.Marshal(wr.Changes[0].NewValue)
	if e != nil {
		return new(proto.User), grpc.Errorf(codes.Internal, e.Error())
	}

	u := proto.User{}

	e = json.Unmarshal(d, &u)
	if e != nil {
		return new(proto.User), grpc.Errorf(codes.Internal, e.Error())
	}

	return &u, nil
}

func (rdb *RethinkDB) GetUser(ctx context.Context, in *proto.GetUserInput) (*proto.User, error) {
	table := rdb.config.Database.Tables["users"].Name

	if in == nil || len(in.Email) < 1 {
		return new(proto.User), grpc.Errorf(codes.InvalidArgument, "missing 'email' argument")
	}

	c, e := r.Table(table).Get(in.Email).Run(rdb.session)
	if e != nil {
		return new(proto.User), grpc.Errorf(codes.Internal, e.Error())
	}

	if c.IsNil() {
		return new(proto.User), grpc.Errorf(codes.NotFound, fmt.Sprintf("no user found with email '%s'", in.Email))
	}

	user := proto.User{}

	e = c.One(&user)
	if e != nil {
		return new(proto.User), grpc.Errorf(codes.Internal, e.Error())
	}

	return &user, nil
}

func (rdb *RethinkDB) GetUserList(ctx context.Context, in *proto.GetUserListInput) (*proto.GetUserListOutput, error) {
	table := rdb.config.Database.Tables["users"].Name

	c, e := r.Table(table).Pluck("email", "name", "surname", "profilePicture").Run(rdb.session)
	if e != nil {
		return new(proto.GetUserListOutput), grpc.Errorf(codes.Internal, e.Error())
	}

	userList := []*proto.UserListItem{}

	if !c.IsNil() {
		e = c.All(&userList)
		if e != nil {
			return new(proto.GetUserListOutput), grpc.Errorf(codes.Internal, e.Error())
		}
	}

	return &proto.GetUserListOutput{UserList: userList}, nil
}

func (rdb *RethinkDB) UpdateUser(ctx context.Context, in *proto.UpdateUserInput) (*proto.User, error) {
	table := rdb.config.Database.Tables["users"].Name

	if in == nil || len(in.Email) < 1 {
		return new(proto.User), grpc.Errorf(codes.InvalidArgument, "'email' is missing")
	}

	if in.UpdateUserInputPayload == nil || (len(in.UpdateUserInputPayload.Location) < 1 && len(in.UpdateUserInputPayload.Name) < 1 && len(in.UpdateUserInputPayload.PhoneNumber) < 1 && len(in.UpdateUserInputPayload.Surname) < 1 && len(in.UpdateUserInputPayload.ProfilePicture) < 1) {
		return new(proto.User), grpc.Errorf(codes.InvalidArgument, "UpdateUserInput payload cannot be empty")
	}

	wr, e := r.Table(table).Get(in.Email).Update(in.UpdateUserInputPayload, r.UpdateOpts{
		ReturnChanges: "always",
	}).RunWrite(rdb.session)
	if e != nil {
		return new(proto.User), grpc.Errorf(codes.Internal, e.Error())
	}

	u := proto.User{}

	if wr.Skipped > 0 {
		return new(proto.User), grpc.Errorf(codes.NotFound, fmt.Sprintf("no user found with email '%s'", in.Email))
	}

	d, e := json.Marshal(wr.Changes[0].NewValue)
	if e != nil {
		return new(proto.User), grpc.Errorf(codes.Internal, e.Error())
	}

	e = json.Unmarshal(d, &u)
	if e != nil {
		return new(proto.User), grpc.Errorf(codes.Internal, e.Error())
	}

	return &u, nil
}

func (rdb *RethinkDB) WatchUser(ctx context.Context, in *proto.WatchUserInput) (<-chan *proto.User, chan error) {
	table := rdb.config.Database.Tables["users"].Name

	ch := make(chan *proto.User)
	e := make(chan error, 1)

	if in == nil || len(in.Email) < 1 {
		e <- grpc.Errorf(codes.InvalidArgument, "argument 'email' is required")
	} else {
		c, err := r.Table(table).Get(in.Email).Changes(r.ChangesOpts{
			IncludeInitial: true,
		}).Run(rdb.session)
		if err != nil {
			e <- grpc.Errorf(codes.Internal, err.Error())
		} else {
			go func(ctx context.Context) {
				<-ctx.Done()
				c.Close()
			}(ctx)

			feed := models.WatchFeed[proto.User]{}

			go func() {
				for c.Next(&feed) {
					if feed.OldVal == nil && feed.NewVal == nil {
						ctx.Done()
						e <- grpc.Errorf(codes.NotFound, fmt.Sprintf("no user found with email '%s'", in.Email))
					}
					if feed.NewVal != nil {
						ch <- feed.NewVal
					}
				}
			}()
		}
	}

	return ch, e
}
