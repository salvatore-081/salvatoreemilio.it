package rethinkdb

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/salvatore.081/salvatoreemilio-it/proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	r "gopkg.in/rethinkdb/rethinkdb-go.v6"
)

func (rdb *RethinkDB) UpdateUser(ctx context.Context, in *proto.UpdateUserInput) (*proto.User, error) {
	if in == nil || len(in.Email) < 1 {
		return new(proto.User), grpc.Errorf(codes.InvalidArgument, "'email' is missing")
	}

	wr, e := r.Table(defaultTable).Get(in.Email).Update(in.Set, r.UpdateOpts{
		ReturnChanges: true,
	}).RunWrite(rdb.session)
	if e != nil {
		return new(proto.User), grpc.Errorf(codes.Internal, e.Error())
	}

	u := proto.User{}

	if len(wr.Changes) == 0 {
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
