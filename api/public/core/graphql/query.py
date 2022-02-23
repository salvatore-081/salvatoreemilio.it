from gql import gql
from ariadne import QueryType
from graphql import GraphQLError
from grpc import RpcError, StatusCode
from models.graphql_responses import InternalServerError, InvalidArgument, NotFound
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
            raise InvalidArgument('email')
        try:
            r = await appState.gRPCCLient.get_user(email)
            return r
        except RpcError as e:
            if e.code() == StatusCode.NOT_FOUND:
                raise NotFound('user', 'email', email)
            raise InternalServerError(e.details())
        except Exception as e:
            raise InternalServerError(str(e))

    return query
