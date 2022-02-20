package resolvers

import (
	"github.com/salvatore.081/salvatoreemilio-it/proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
)

func (s *Server) WatchUser(in *proto.WatchUserInput, stream proto.Internal_WatchUserServer) error {
	ch, e := s.Db.WatchUser(stream.Context(), in)
	if e != nil {
		return e
	}

	for u := range ch {
		if e := stream.Send(u); e != nil {
			return grpc.Errorf(codes.Internal, e.Error())
		}
	}

	return e
}
