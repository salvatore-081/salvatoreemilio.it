package rethinkdb

import (
	"context"
	"encoding/json"
	"errors"

	r "gopkg.in/rethinkdb/rethinkdb-go.v6"

	"github.com/salvatore.081/salvatoreemilio-it-graphql-server/models"
)

func (rdb *RethinkDB) CreateUser(ctx context.Context, input models.CreateUserInput) (*models.User, error) {
	wr, e := r.Table(defaultTable).Insert(input, r.InsertOpts{
		ReturnChanges: true,
	}).RunWrite(rdb.session)
	if e != nil {
		return nil, e
	}

	if len(wr.Changes) == 0 {
		return nil, errors.New("createUser unexpected error")
	}

	d, e := json.Marshal(wr.Changes[0].NewValue)
	if e != nil {
		return nil, e
	}
	u := models.User{}

	e = json.Unmarshal(d, &u)
	if e != nil {
		return nil, e
	}

	return &u, nil
}
