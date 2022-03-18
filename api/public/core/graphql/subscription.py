from ariadne import SubscriptionType
from grpc import StatusCode
from grpc.aio import AioRpcError
from state.appState import AppState
from exceptions import graphql as graphql_exceptions, base as base_exceptions


def getSubscription(appState: AppState) -> SubscriptionType:
    subscription = SubscriptionType()

    @subscription.source('watchUser')
    async def resolve_watch_user_source(req, info, email):
        if not email:
            yield graphql_exceptions.InvalidArgument('email')
            return
        try:
            access_token: str = info.context['access_token']
            introspection = appState.keycloak.introspect_token(access_token)
            appState.keycloak.check_active(introspection)
            appState.keycloak.check_view_users(introspection, email)

            async for user in appState.gRPCCLient.watch_user(email):
                appState.keycloak.check_active(introspection)
                appState.keycloak.check_view_users(introspection, email)
                yield user
        except base_exceptions.BadRequest:
            yield graphql_exceptions.BadRequest("bad request")
            return
        except base_exceptions.Forbidden:
            yield graphql_exceptions.Forbidden()
            return
        except base_exceptions.Unauthorized:
            yield graphql_exceptions.Unauthorized()
            return
        except AioRpcError as e:
            if e.code() == StatusCode.NOT_FOUND:
                yield graphql_exceptions.NotFound('user', 'email', email)
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
