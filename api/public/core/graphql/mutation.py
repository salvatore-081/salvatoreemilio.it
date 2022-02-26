from gql import gql
from ariadne import MutationType
from exceptions import graphql as graphql_exceptions, base as base_exceptions
from models.auth import LogoutResponse
from state.appState import AppState
from keycloak.exceptions import KeycloakAuthenticationError, KeycloakGetError


LOGIN = gql(
    """
    mutation login($input: LoginInput!){
        getUser(input: $input){
            access_token
            expires_in
            refresh_expires_in
            refresh_token
            token_type
            session_state
            scope
        }
    }
    """
)


def getMutation(appState: AppState) -> MutationType:
    mutation = MutationType()

    @mutation.field("login")
    async def resolve_login(_, info, input):
        if not 'email' in input or len(input['email']) < 1:
            raise graphql_exceptions.InvalidArgument('email')
        if not 'password' in input or len(input['password']) < 1:
            raise graphql_exceptions.InvalidArgument('password')
        try:
            login = appState.keycloak.login(
                input['email'], input['password'], input['totp'] if 'totp' in input else None)
            return login
        except KeycloakAuthenticationError:
            raise graphql_exceptions.Unauthorized()
        except Exception as e:
            raise graphql_exceptions.InternalServerError(str(e))

    @mutation.field("logout")
    async def resolve_logout(_, info, refresh_token):
        try:
            request = info.context["request"]
            auth: str = request.headers.get('Authorization', None)
            if not auth or not auth.startswith("Bearer ") or len(auth) < 7:
                return graphql_exceptions.BadRequest("invalid Authorization")

            if not refresh_token or len(refresh_token) < 1:
                return graphql_exceptions.InvalidArgument('refresh_token')

            access_token = auth[7:]
            introspection = appState.keycloak.introspect_token(
                access_token)
            appState.keycloak.check_active(introspection)

            appState.keycloak.logout(refresh_token)
            return LogoutResponse(refresh_token=refresh_token).dict()
        except base_exceptions.BadRequest:
            return graphql_exceptions.BadRequest("bad request")
        except base_exceptions.Forbidden:
            return graphql_exceptions.Forbidden()
        except base_exceptions.Unauthorized:
            return graphql_exceptions.Unauthorized()
        except KeycloakGetError:
            return graphql_exceptions.BadRequest(
                message="invalid refresh_token")
        except Exception as e:
            return graphql_exceptions.InternalServerError(str(e))

    return mutation
