from gql import gql
from ariadne import QueryType
from grpc import RpcError, StatusCode
from exceptions import graphql as graphql_exceptions, base as base_exceptions
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
        try:
            request = info.context["request"]
            auth: str = request.headers.get('Authorization', None)
            if not auth or not auth.startswith("Bearer ") or len(auth) < 7:
                return graphql_exceptions.BadRequest("invalid Authorization")

            if not email:
                return graphql_exceptions.InvalidArgument('email')

            access_token = auth[7:]
            introspection = appState.keycloak.introspect_token(
                access_token)
            appState.keycloak.check_active(introspection)
            appState.keycloak.check_view_users(introspection, email)
            r = await appState.gRPCCLient.get_user(email)
            return r
        except base_exceptions.BadRequest:
            return graphql_exceptions.BadRequest("bad request")
        except base_exceptions.Forbidden:
            return graphql_exceptions.Forbidden()
        except base_exceptions.Unauthorized:
            return graphql_exceptions.Unauthorized()
        except RpcError as e:
            if e.code() == StatusCode.NOT_FOUND:
                return graphql_exceptions.NotFound('user', 'email', email)
            if e.code() == StatusCode.INVALID_ARGUMENT:
                return graphql_exceptions.BadRequest('bad request')
            return graphql_exceptions.InternalServerError(e.details())
        except Exception as e:
            return graphql_exceptions.InternalServerError(str(e))

    return query
