from fastapi import APIRouter, Depends
from fastapi.params import Depends
from state.appState import AppState
from deps.gRPCClient import GRPCClient
from deps.keycloak import Keycloak
from models.project import Projects, Project, AddProjectInput, UpdateProjectInputPayload, DeleteProjectOutput
from google.protobuf.json_format import MessageToDict
from fastapi.security import HTTPBearer
from exceptions import rest as rest_exceptions


def newProjectsRouter(appState: AppState):
    router = APIRouter()
    token_auth_scheme = HTTPBearer()

    @router.get("/{email}", response_model=Projects, responses={400: {"model": rest_exceptions.BadRequest}, 404: {"model": rest_exceptions.NotFound}, 500: {"model": rest_exceptions.InternalServerError}},  response_model_exclude_none=True)
    async def get_projects(email: str, gRPCClient: GRPCClient = Depends(appState.select_gPRCClient)):
        try:
            r = await gRPCClient.get_projects(email)
            return MessageToDict(r)
        except Exception as e:
            raise e
    
    @router.post("", response_model=Project, responses={400: {"model": rest_exceptions.BadRequest},  500: {"model": rest_exceptions.InternalServerError}}, response_model_exclude_none=True)
    async def add_project(addProjectInput: AddProjectInput, gRPCClient: GRPCClient = Depends(appState.select_gPRCClient), keycloak: Keycloak = Depends(appState.select_keycloak), token: str = Depends(token_auth_scheme)):
        try:
            introspection = keycloak.introspect_token(token.credentials)
            keycloak.check_active(introspection)
            keycloak.check_manage_users(introspection, addProjectInput.email)

            r = await gRPCClient.add_project(addProjectInput)
            return MessageToDict(r)
        except Exception as e:
            raise e

    @router.put("/{id}", response_model=Project, responses={400: {"model": rest_exceptions.BadRequest}, 404: {"model": rest_exceptions.NotFound}, 500: {"model": rest_exceptions.InternalServerError}}, response_model_exclude_none=True)
    async def update_project(id: str, payload: UpdateProjectInputPayload, gRPCClient: GRPCClient = Depends(appState.select_gPRCClient), keycloak: Keycloak = Depends(appState.select_keycloak), token: str = Depends(token_auth_scheme)):
        try:
            introspection = keycloak.introspect_token(token.credentials)
            keycloak.check_active(introspection)
            
            project = await gRPCClient.get_project(id)
            keycloak.check_manage_users(introspection, project.email)

            r = await gRPCClient.update_project(id, payload)
            return MessageToDict(r)
        except Exception as e:
            raise e
    
    @router.delete("/{id}", response_model=DeleteProjectOutput, responses={400: {"model": rest_exceptions.BadRequest}, 404: {"model": rest_exceptions.NotFound}, 500: {"model": rest_exceptions.InternalServerError}}, response_model_exclude_none=True)
    async def delete_project(id: str, gRPCClient: GRPCClient = Depends(appState.select_gPRCClient), keycloak: Keycloak = Depends(appState.select_keycloak), token: str = Depends(token_auth_scheme)):
        try:
            introspection = keycloak.introspect_token(token.credentials)
            keycloak.check_active(introspection)

            project = await gRPCClient.get_project(id)
            keycloak.check_manage_users(introspection, project.email)

            deleted_project = await gRPCClient.delete_project(id)
            return MessageToDict(delete_project)
        except Exception as e:
            raise e

    return router

