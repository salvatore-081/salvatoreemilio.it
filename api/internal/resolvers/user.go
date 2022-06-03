package resolvers

import (
	"context"

	"github.com/salvatore.081/salvatoreemilio-it/proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
)

func (s *Server) AddUser(ctx context.Context, in *proto.AddUserInput) (*proto.User, error) {
	return s.Db.AddUser(ctx, in)
}

func (s *Server) GetUser(ctx context.Context, in *proto.GetUserInput) (*proto.User, error) {
	return s.Db.GetUser(ctx, in)
}

func (s *Server) GetUserList(ctx context.Context, in *proto.GetUserListInput) (*proto.GetUserListOutput, error) {
	return s.Db.GetUserList(ctx, in)
}

func (s *Server) UpdateUser(ctx context.Context, in *proto.UpdateUserInput) (*proto.User, error) {
	return s.Db.UpdateUser(ctx, in)
}

func (s *Server) WatchUser(in *proto.WatchUserInput, stream proto.Internal_WatchUserServer) error {
	ch, e := s.Db.WatchUser(stream.Context(), in)

	go func() {
		for u := range ch {
			if err := stream.Send(u); err != nil {
				e <- grpc.Errorf(codes.Internal, err.Error())
			}
		}
	}()

	return <-e
}