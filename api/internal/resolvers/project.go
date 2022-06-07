package resolvers

import (
	"context"

	"github.com/golang/protobuf/ptypes/empty"
	"github.com/salvatore.081/salvatoreemilio-it/proto"
)

func (s *Server) AddProject(ctx context.Context, in *proto.AddProjectInput) (*proto.Project, error) {
	return s.Db.AddProject(ctx, in)
}

func (s *Server) GetProjects(ctx context.Context, in *proto.GetProjectsInput) (*proto.GetProjectsOutput, error) {
	return s.Db.GetProjects(ctx, in)
}

func (s *Server) DeleteProject(ctx context.Context, in *proto.DeleteProjectInput) (*empty.Empty, error) {
	return s.Db.DeleteProject(ctx, in)
}
