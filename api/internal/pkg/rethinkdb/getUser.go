package rethinkdb

import (
	"context"

	r "gopkg.in/rethinkdb/rethinkdb-go.v6"

	"github.com/salvatore.081/salvatoreemilio-it-internal-api/models"
)

func (rdb *RethinkDB) GetUser(ctx context.Context, email string) (*models.User, error) {
	c, e := r.Table(defaultTable).Get(email).Run(rdb.session)
	if e != nil {
		return nil, e
	}

	users := []*models.User{}

	e = c.All(&users)
	if e != nil {
		return nil, e
	}

	if len(users) == 0 {
		return nil, nil
	}

	return users[0], nil
}
