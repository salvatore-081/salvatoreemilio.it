package graph

import (
	"github.com/salvatore.081/salvatoreemilio-it-graphql-server/pkg/rethinkdb"
)

// This file will not be regenerated automatically.
//
// It serves as dependency injection for your app, add any dependencies you require here.

type Resolver struct {
	DB *rethinkdb.RethinkDB
}
