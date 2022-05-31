package rethinkdb

import (
	"context"

	"github.com/salvatore.081/salvatoreemilio-it/proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	r "gopkg.in/rethinkdb/rethinkdb-go.v6"
)

func (rdb *RethinkDB) GetUserList(ctx context.Context, in *proto.GetUserListInput) (*proto.GetUserListOutput, error) {
	c, e := r.Table(usersTable).Pluck("email", "name", "surname", "profilePicture").Run(rdb.session)
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
