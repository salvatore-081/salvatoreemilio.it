from gql import gql
from ariadne import QueryType
from grpc import RpcError, StatusCode
from exceptions import graphql as graphql_exceptions
from state.appState import AppState

GET_USER = gql(
    """
    query getUser($email: String!){
        getUser(email: $email){
            email
            name
            surname
            phoneNumber
            currentLocation
        }
    }
    """
)


def getQuery(appState: AppState) -> QueryType:
    query = QueryType()

    @query.field("getUser")
    async def resolve_getUser(_, info, email):
        if not email:
            raise graphql_exceptions.InvalidArgument('email')
        try:
            r = await appState.gRPCCLient.get_user(email)
            return r
        except RpcError as e:
            if e.code() == StatusCode.NOT_FOUND:
                raise graphql_exceptions.NotFound('user', 'email', email)
            raise graphql_exceptions.InternalServerError(e.details())
        except Exception as e:
            raise graphql_exceptions.InternalServerError(str(e))

    return query
