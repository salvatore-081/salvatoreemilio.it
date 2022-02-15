package rethinkdb

import (
	"context"
	"fmt"

	"github.com/salvatore.081/salvatoreemilio-it/proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	r "gopkg.in/rethinkdb/rethinkdb-go.v6"
)

func (rdb *RethinkDB) GetUser(ctx context.Context, in *proto.GetUserInput) (*proto.User, error) {
	if in == nil || len(in.Email) < 1 {
		return new(proto.User), grpc.Errorf(codes.InvalidArgument, "missing 'email' argument")
	}

	c, e := r.Table(defaultTable).Get(in.Email).Run(rdb.session)
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
