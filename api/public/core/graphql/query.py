from ariadne import QueryType
from grpc import RpcError, StatusCode
from exceptions import graphql as graphql_exceptions
from state.appState import AppState


def getQuery(appState: AppState) -> QueryType:
    query = QueryType()

    @query.field("getUser")
    async def resolve_getUser(_, info, email):
        try:
            if not email:
                return graphql_exceptions.InvalidArgument('email')
            r = await appState.gRPCCLient.get_user(email)
            return r
        except RpcError as e:
            if e.code() == StatusCode.NOT_FOUND:
                return graphql_exceptions.NotFound('user', 'email', email)
            if e.code() == StatusCode.INVALID_ARGUMENT:
                return graphql_exceptions.BadRequest('bad request')
            return graphql_exceptions.InternalServerError(e.details())
        except Exception as e:
            return graphql_exceptions.InternalServerError(str(e))

    return query
