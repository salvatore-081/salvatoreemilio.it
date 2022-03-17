package resolvers

import (
	"github.com/salvatore.081/salvatoreemilio-it/proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
)

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
