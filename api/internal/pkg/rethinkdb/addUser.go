package rethinkdb

import (
	"context"
	"encoding/json"

	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	r "gopkg.in/rethinkdb/rethinkdb-go.v6"

	"github.com/salvatore.081/salvatoreemilio-it/proto"
)

func (rdb *RethinkDB) AddUser(ctx context.Context, in *proto.AddUserInput) (*proto.User, error) {
	if in == nil || len(in.Email) < 1 {
		return new(proto.User), grpc.Errorf(codes.InvalidArgument, "argument 'email' is required")
	}

	wr, e := r.Table(defaultTable).Insert(in, r.InsertOpts{
		ReturnChanges: true,
	}).RunWrite(rdb.session)
	if e != nil {
		return new(proto.User), grpc.Errorf(codes.Internal, e.Error())
	}

	if len(wr.Changes) == 0 {
		return new(proto.User), grpc.Errorf(codes.Internal, "insert error")
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
