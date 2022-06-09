from ariadne import SubscriptionType
from grpc import StatusCode
from grpc.aio import AioRpcError
from state.appState import AppState
from exceptions import graphql as graphql_exceptions


def newSubscription(appState: AppState) -> SubscriptionType:
    subscription = SubscriptionType()

    @subscription.source('watchUser')
    async def resolve_watch_user_source(req, info, email):
        if not email:
            yield graphql_exceptions.InvalidArgument('email')
            return
        try:
            async for user in appState.gRPCCLient.watch_user(email):
                yield user
        except AioRpcError as e:
            if e.code() == StatusCode.NOT_FOUND:
                yield graphql_exceptions.NotFound(e.details())
                return
            yield graphql_exceptions.InternalServerError(e.details())
            return
        except Exception as e:
            yield e
            return

    @subscription.field('watchUser')
    async def resolve_watch_user_field(source, info, email):
        try:
            return source
        except Exception as e:
            return graphql_exceptions.InternalServerError(str(e))

    return subscription
