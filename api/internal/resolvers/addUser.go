package resolvers

import (
	"context"

	"github.com/salvatore.081/salvatoreemilio-it/proto"
)

func (s *Server) AddUser(ctx context.Context, in *proto.AddUserInput) (*proto.User, error) {
	return s.Db.AddUser(ctx, in)
}
