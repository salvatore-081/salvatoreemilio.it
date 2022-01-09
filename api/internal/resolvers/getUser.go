package resolvers

import (
	"context"

	"github.com/salvatore.081/salvatoreemilio-it/proto"
)

func (s *Server) GetUser(ctx context.Context, in *proto.GetUserInput) (*proto.User, error) {
	return s.Db.GetUser(ctx, in)
}
