package rethinkdb

import (
	"context"
	"fmt"

	"github.com/rs/zerolog/log"
	"github.com/salvatore.081/salvatoreemilio-it/proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	r "gopkg.in/rethinkdb/rethinkdb-go.v6"
)

type watchUserFeed struct {
	NewVal *proto.User `json:"new_val,omitempty"`
	OldVal *proto.User `json:"old_val,omitempty"`
}

func (rdb *RethinkDB) WatchUser(ctx context.Context, in *proto.WatchUserInput) (<-chan *proto.User, chan error) {
	ch := make(chan *proto.User)
	e := make(chan error, 1)

	if in == nil || len(in.Email) < 1 {
		e <- grpc.Errorf(codes.InvalidArgument, "argument 'email' is required")
	} else {
		c, err := r.Table(usersTable).Get(in.Email).Changes(r.ChangesOpts{
			IncludeInitial: true,
		}).Run(rdb.session)
		if err != nil {
			e <- grpc.Errorf(codes.Internal, err.Error())
		} else {
			go func(ctx context.Context) {
				<-ctx.Done()
				log.Debug().Msg("WatchUser cursor closed")
				c.Close()
			}(ctx)

			feed := watchUserFeed{}

			go func() {
				for c.Next(&feed) {
					if feed.OldVal == nil && feed.NewVal == nil {
						ctx.Done()
						e <- grpc.Errorf(codes.NotFound, fmt.Sprintf("no user found with email '%s'", in.Email))
					}
					if feed.NewVal != nil {
						ch <- feed.NewVal
					}
				}
			}()
		}
	}

	return ch, e
}
