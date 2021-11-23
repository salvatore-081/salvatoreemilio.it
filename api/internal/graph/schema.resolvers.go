package graph

// This file will be automatically regenerated based on the schema, any resolver implementations
// will be copied through when generating and any unknown code will be moved to the end.

import (
	"context"

	"github.com/salvatore.081/salvatoreemilio-it-graphql-server/graph/generated"
	"github.com/salvatore.081/salvatoreemilio-it-graphql-server/models"
)

func (r *mutationResolver) CreateUser(ctx context.Context, input models.CreateUserInput) (*models.User, error) {
	return r.DB.CreateUser(ctx, input)
}

func (r *mutationResolver) UpdateUser(ctx context.Context, input models.UpdateUserInput) (*models.User, error) {
	return r.DB.UpdateUser(ctx, input)
}

func (r *queryResolver) GetUser(ctx context.Context, email string) (*models.User, error) {
	return r.DB.GetUser(ctx, email)
}

func (r *subscriptionResolver) WatchUser(ctx context.Context, email string) (<-chan *models.User, error) {
	return r.DB.WatchUser(ctx, email)
}

// Mutation returns generated.MutationResolver implementation.
func (r *Resolver) Mutation() generated.MutationResolver { return &mutationResolver{r} }

// Query returns generated.QueryResolver implementation.
func (r *Resolver) Query() generated.QueryResolver { return &queryResolver{r} }

// Subscription returns generated.SubscriptionResolver implementation.
func (r *Resolver) Subscription() generated.SubscriptionResolver { return &subscriptionResolver{r} }

type mutationResolver struct{ *Resolver }
type queryResolver struct{ *Resolver }
type subscriptionResolver struct{ *Resolver }
