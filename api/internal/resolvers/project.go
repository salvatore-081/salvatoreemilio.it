package resolvers

import (
	"context"

	"github.com/golang/protobuf/ptypes/empty"
	"github.com/salvatore.081/salvatoreemilio-it/proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
)

func (s *Server) AddProject(ctx context.Context, in *proto.AddProjectInput) (*proto.Project, error) {
	return s.Db.AddProject(ctx, in)
}

func (s *Server) GetProject(ctx context.Context, in *proto.GetProjectInput) (*proto.Project, error) {
	return s.Db.GetProject(ctx, in)
}

func (s *Server) GetProjects(ctx context.Context, in *proto.GetProjectsInput) (*proto.GetProjectsOutput, error) {
	return s.Db.GetProjects(ctx, in)
}

func (s *Server) UpdateProject(ctx context.Context, in *proto.UpdateProjectInput) (*proto.Project, error) {
	return s.Db.UpdateProject(ctx, in)
}

func (s *Server) DeleteProject(ctx context.Context, in *proto.DeleteProjectInput) (*empty.Empty, error) {
	return s.Db.DeleteProject(ctx, in)
}

func (s *Server) WatchProjects(in *proto.WatchProjectsInput, stream proto.Internal_WatchProjectsServer) error {
	ch, e := s.Db.WatchProjects(stream.Context(), in)

	go func() {
		for p := range ch {
			if err := stream.Send(p); err != nil {
				e <- grpc.Errorf(codes.Internal, err.Error())
			}
		}
	}()

	return <-e
}
