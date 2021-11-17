package rethinkdb

import (
	"context"

	"github.com/salvatore.081/salvatoreemilio-it-graphql-server/models"
	r "gopkg.in/rethinkdb/rethinkdb-go.v6"
)

func (rdb *RethinkDB) WatchUser(ctx context.Context, email string) (<-chan *models.User, error) {
	ch := make(chan *models.User)

	c, e := r.Table(defaultTable).Get(email).Changes(r.ChangesOpts{
		IncludeInitial: true,
	}).Run(rdb.session)
	if e != nil {
		return nil, e
	}

	go func(ctx context.Context) {
		<-ctx.Done()
		c.Close()
	}(ctx)

	feed := models.WatchUserFeed{}

	go func() {
		for c.Next(&feed) {
			if feed.NewVal != nil {
				ch <- feed.NewVal
			}
		}
	}()

	return ch, nil
}
