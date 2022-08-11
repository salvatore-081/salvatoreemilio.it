from ariadne import MutationType
from grpc import RpcError, StatusCode
from models.user import UpdateUserInputPayload
from exceptions import graphql as graphql_exceptions, base as base_exceptions
from models.auth import LogoutResponse
from state.appState import AppState
from keycloak.exceptions import KeycloakAuthenticationError, KeycloakGetError


def newMutation(appState: AppState) -> MutationType:
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

    @mutation.field("updateUser")
    async def resolve_update_user(_, info, input):
        try:
            request = info.context["request"]
            auth: str = request.headers.get('Authorization', None)
            if not auth or not auth.startswith("Bearer ") or len(auth) < 7:
                return graphql_exceptions.BadRequest("invalid Authorization")
            if not 'email' in input or len(input['email']) < 1:
                return graphql_exceptions.InvalidArgument('email')
            if not 'payload' in input or all(v == None or len(v) < 1 for v in input['payload'].values()):
                return graphql_exceptions.InvalidArgument('payload')

            access_token = auth[7:]
            introspection = appState.keycloak.introspect_token(
                access_token)
            appState.keycloak.check_active(introspection)
            appState.keycloak.check_manage_users(introspection, input['email'])
            r = await appState.gRPCClient.update_user(input['email'], UpdateUserInputPayload(**input['payload']))
            return r
        except base_exceptions.BadRequest:
            return graphql_exceptions.BadRequest("bad request")
        except base_exceptions.Forbidden:
            return graphql_exceptions.Forbidden()
        except base_exceptions.Unauthorized:
            return graphql_exceptions.Unauthorized()
        except RpcError as e:
            if e.code() == StatusCode.NOT_FOUND:
                return graphql_exceptions.NotFound(e.details())
            if e.code() == StatusCode.INVALID_ARGUMENT:
                return graphql_exceptions.BadRequest('bad request')
            return graphql_exceptions.InternalServerError(e.details())
        except Exception as e:
            return graphql_exceptions.InternalServerError(str(e))
    
    @mutation.field("addProject")
    async def resolve_addProject(_, info, input):
        try:
            request = info.context["request"]
            auth: str = request.headers.get('Authorization', None)
            if not auth or not auth.startswith("Bearer ") or len(auth) < 7:
                return graphql_exceptions.BadRequest("invalid Authorization")
            if not 'email' in input or len(input['email']) < 1:
                return graphql_exceptions.InvalidArgument('email')
            if all(v == None or len(v) < 1 for v in input.values()):
                return graphql_exceptions.InvalidArgument('input')

            access_token = auth[7:]
            introspection = appState.keycloak.introspect_token(access_token)
            appState.keycloak.check_active(introspection)
            appState.keycloak.check_manage_users(introspection, input['email'])

            r = await appState.gRPCClient.add_project(input)
            return r
        except base_exceptions.BadRequest:
            return graphql_exceptions.BadRequest("bad request")
        except base_exceptions.Forbidden:
            return graphql_exceptions.Forbidden()
        except base_exceptions.Unauthorized:
            return graphql_exceptions.Unauthorized()
        except RpcError as e:
            if e.code() == StatusCode.INVALID_ARGUMENT:
                return graphql_exceptions.BadRequest('bad request')
            return graphql_exceptions.InternalServerError(e.details())
        except Exception as e:
            return graphql_exceptions.InternalServerError(str(e))
    
    @mutation.field("updateProject")
    async def resolve_updateProject(_, info, input):
        try:
            request = info.context["request"]
            auth: str = request.headers.get('Authorization', None)
            if not auth or not auth.startswith("Bearer ") or len(auth) < 7:
                return graphql_exceptions.BadRequest("invalid Authorization")
            if not 'id' in input or len(input['id']) < 1:
                return graphql_exceptions.InvalidArgument('id')
            if not 'payload' in input or all(v == None for v in input['payload'].values()):
                return graphql_exceptions.InvalidArgument('payload')

            access_token = auth[7:]
            introspection = appState.keycloak.introspect_token(access_token)
            appState.keycloak.check_active(introspection)

            project = await appState.gRPCClient.get_project(input['id'])
            appState.keycloak.check_manage_users(introspection, project.email)

            r = await appState.gRPCClient.update_project(input['id'], input['payload'])
            return r
        except base_exceptions.BadRequest:
            return graphql_exceptions.BadRequest("bad request")
        except base_exceptions.Forbidden:
            return graphql_exceptions.Forbidden()
        except base_exceptions.Unauthorized:
            return graphql_exceptions.Unauthorized()
        except RpcError as e:
            if e.code() == StatusCode.NOT_FOUND:
                return graphql_exceptions.NotFound(e.details())
            if e.code() == StatusCode.INVALID_ARGUMENT:
                return graphql_exceptions.BadRequest('bad request')
            return graphql_exceptions.InternalServerError(e.details())
        except Exception as e:
            return graphql_exceptions.InternalServerError(str(e))
        
    @mutation.field("deleteProject")
    async def resolve_deleteProject(_, info, id):
        try:
            request = info.context["request"]
            auth: str = request.headers.get('Authorization', None)
            if not auth or not auth.startswith("Bearer ") or len(auth) < 7:
                return graphql_exceptions.BadRequest("invalid Authorization")
            if not id or len(id) < 1:
                return graphql_exceptions.InvalidArgument('id')

            access_token = auth[7:]
            introspection = appState.keycloak.introspect_token(access_token)
            appState.keycloak.check_active(introspection)

            project = await appState.gRPCClient.get_project(id)
            appState.keycloak.check_manage_users(introspection, project.email)

            r = await appState.gRPCClient.delete_project(id)
            return r
        except base_exceptions.BadRequest:
            return graphql_exceptions.BadRequest("bad request")
        except base_exceptions.Forbidden:
            return graphql_exceptions.Forbidden()
        except base_exceptions.Unauthorized:
            return graphql_exceptions.Unauthorized()
        except RpcError as e:
            if e.code() == StatusCode.NOT_FOUND:
                return graphql_exceptions.NotFound(e.details())
            if e.code() == StatusCode.INVALID_ARGUMENT:
                return graphql_exceptions.BadRequest('bad request')
            return graphql_exceptions.InternalServerError(e.details())
        except Exception as e:
            return graphql_exceptions.InternalServerError(str(e))

    return mutation
