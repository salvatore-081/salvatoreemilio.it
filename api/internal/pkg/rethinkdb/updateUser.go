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

	if in.UpdateUserInputPayload == nil || (len(in.UpdateUserInputPayload.CurrentLocation) < 1 && len(in.UpdateUserInputPayload.Name) < 1 && len(in.UpdateUserInputPayload.PhoneNumber) < 1 && len(in.UpdateUserInputPayload.Surname) < 1) {
		return new(proto.User), grpc.Errorf(codes.InvalidArgument, "UpdateUserInput payload cannot be empty")
	}

	wr, e := r.Table(defaultTable).Get(in.Email).Update(in.UpdateUserInputPayload, r.UpdateOpts{
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
