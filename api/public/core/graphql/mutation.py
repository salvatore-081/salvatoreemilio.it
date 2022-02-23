from gql import gql
from ariadne import MutationType
from models.graphql_responses import InternalServerError, InvalidArgument, Unauthorized
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
        if not 'email' in input:
            raise InvalidArgument('email')
        if not 'password' in input:
            raise InvalidArgument('password')
        try:
            login = appState.keycloak.login(
                input['email'], input['password'], input['totp'] if 'totp' in input else None)
            return login
        except KeycloakAuthenticationError:
            raise Unauthorized()
        except Exception as e:
            raise InternalServerError(str(e))

    return mutation
