package resolvers

import (
	"context"

	"github.com/salvatore.081/salvatoreemilio-it/proto"
)

func (s *Server) UpdateUser(ctx context.Context, in *proto.UpdateUserInput) (*proto.User, error) {
	return s.Db.UpdateUser(ctx, in)
}
