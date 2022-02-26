from gql import gql
from ariadne import MutationType
from exceptions import graphql as graphql_exceptions
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
            if not refresh_token or len(refresh_token) < 1:
                raise graphql_exceptions.InvalidArgument('refresh_token')
            appState.keycloak.logout(refresh_token)
            return LogoutResponse(refresh_token=refresh_token).dict()
        except KeycloakGetError:
            raise graphql_exceptions.BadRequest(
                message="invalid refresh_token")
        except Exception as e:
            raise graphql_exceptions.InternalServerError(str(e))

    return mutation
