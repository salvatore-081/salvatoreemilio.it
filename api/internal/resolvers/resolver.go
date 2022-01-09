package resolvers

import (
	"github.com/salvatore.081/salvatoreemilio-it/pkg/rethinkdb"
	pb "github.com/salvatore.081/salvatoreemilio-it/proto"
)

type Server struct {
	pb.UnimplementedInternalServer
	Db *rethinkdb.RethinkDB
}
