package resolvers

import (
	"context"

	"github.com/salvatore.081/salvatoreemilio-it/proto"
)

func (s *Server) GetUserList(ctx context.Context, in *proto.GetUserListInput) (*proto.GetUserListOutput, error) {
	return s.Db.GetUserList(ctx, in)
}
