package rethinkdb

import (
	"context"
	"encoding/json"
	"errors"

	"github.com/salvatore.081/salvatoreemilio-it-internal-api/models"
	r "gopkg.in/rethinkdb/rethinkdb-go.v6"
)

func (rdb *RethinkDB) UpdateUser(ctx context.Context, input models.UpdateUserInput) (*models.User, error) {
	wr, e := r.Table(defaultTable).Get(input.Email).Update(input.Set, r.UpdateOpts{
		ReturnChanges: true,
	}).RunWrite(rdb.session)
	if e != nil {
		return nil, e
	}

	u := models.User{}

	if len(wr.Changes) == 0 {
		return nil, errors.New("updateUser unexpected error")
	}

	d, e := json.Marshal(wr.Changes[0].NewValue)
	if e != nil {
		return nil, e
	}

	e = json.Unmarshal(d, &u)

	if e != nil {
		return nil, e
	}

	return &u, nil
}
