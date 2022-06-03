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
                return graphql_exceptions.NotFound(e.details())
            if e.code() == StatusCode.INVALID_ARGUMENT:
                return graphql_exceptions.BadRequest('bad request')
            return graphql_exceptions.InternalServerError(e.details())
        except Exception as e:
            return graphql_exceptions.InternalServerError(str(e))

    @query.field("getUserList")
    async def resolve_getUserList(_, info):
        try:
            r = await appState.gRPCCLient.get_user_list()
            return r
        except RpcError as e:
            if e.code() == StatusCode.NOT_FOUND:
                return graphql_exceptions.NotFound(e.details())
            return graphql_exceptions.InternalServerError(e.details())
        except Exception as e:
            return graphql_exceptions.InternalServerError(str(e))

    return query
