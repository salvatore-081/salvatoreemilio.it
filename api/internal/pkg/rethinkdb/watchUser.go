package rethinkdb

import (
	"context"

	"github.com/salvatore.081/salvatoreemilio-it/proto"
	"google.golang.org/grpc"
	"google.golang.org/grpc/codes"
	r "gopkg.in/rethinkdb/rethinkdb-go.v6"
)

type watchUserFeed struct {
	NewVal *proto.User `json:"new_val,omitempty"`
	OldVal *proto.User `json:"old_val,omitempty"`
}

func (rdb *RethinkDB) WatchUser(ctx context.Context, in *proto.WatchUserInput) (<-chan *proto.User, error) {
	ch := make(chan *proto.User)

	if in == nil || len(in.Email) < 1 {
		return ch, grpc.Errorf(codes.InvalidArgument, "argument 'email' is required")
	}

	c, e := r.Table(defaultTable).Get(in.Email).Changes(r.ChangesOpts{
		IncludeInitial: true,
	}).Run(rdb.session)
	if e != nil {
		return ch, grpc.Errorf(codes.Internal, e.Error())
	}

	go func(ctx context.Context) {
		<-ctx.Done()
		c.Close()
	}(ctx)

	feed := watchUserFeed{}

	go func() {
		for c.Next(&feed) {
			if feed.NewVal != nil {
				ch <- feed.NewVal
			}
		}
	}()

	return ch, nil
}
