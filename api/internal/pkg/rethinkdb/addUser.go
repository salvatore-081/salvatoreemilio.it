package rethinkdb

import (
	"context"
	"encoding/json"
	"errors"

	r "gopkg.in/rethinkdb/rethinkdb-go.v6"

	"github.com/salvatore.081/salvatoreemilio-it-internal-api/models"
)

func (rdb *RethinkDB) AddUser(ctx context.Context, input models.AddUserInput) (*models.User, error) {
	wr, e := r.Table(defaultTable).Insert(input, r.InsertOpts{
		ReturnChanges: true,
	}).RunWrite(rdb.session)
	if e != nil {
		return nil, e
	}

	if len(wr.Changes) == 0 {
		return nil, errors.New("addUser unexpected error")
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
