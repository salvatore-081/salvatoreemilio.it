from fastapi import Request
from grpc import RpcError, StatusCode
from grpc.aio import insecure_channel
from models import project as project_models
from deps.config import GRPCServerConfig
from proto.internal_pb2_grpc import InternalStub
from proto.internal_pb2 import DeleteProjectInput, GetProjectInput, GetUserInput, GetUserListInput, UpdateUserInput, UpdateUserInputPayload, WatchProjectsInput, WatchUserInput, GetProjectsInput, AddProjectInput, UpdateProjectInput, UpdateProjectInputPayload
from starlette.responses import JSONResponse
from exceptions import rest as rest_exceptions
class GRPCClient():
    def __init__(self, config: GRPCServerConfig) -> None:
        try:
            self.config = config
            self.url = f"{self.config.host}:{self.config.port}"
        except Exception as e:
            raise e

    async def get_user(self, email: str):
        try:
            async with insecure_channel(self.url) as ch:
                st = InternalStub(ch)
                getUser = await st.GetUser(GetUserInput(email=email))
                return getUser
        except Exception as e:
            raise e

    async def get_user_list(self):
        try:
            async with insecure_channel(self.url) as ch:
                st = InternalStub(ch)
                getUserList = await st.GetUserList(GetUserListInput())
                return getUserList
        except Exception as e:
            raise e

    async def update_user(self, email: str, payload: UpdateUserInputPayload):
        try:
            async with insecure_channel(self.url) as ch:
                st = InternalStub(ch)
                updateUser = await st.UpdateUser(UpdateUserInput(email=email, updateUserInputPayload=UpdateUserInputPayload(**payload.dict())))
                return updateUser
        except Exception as e:
            raise e

    async def watch_user(self, email: str):
        try:
            async with insecure_channel(self.url) as ch:
                st = InternalStub(ch)
                async for user in st.WatchUser(WatchUserInput(email=email)):
                    yield user
        except Exception as e:
            raise e

    async def get_project(self, id: str):
        try:
            async with insecure_channel(self.url) as ch:
                st = InternalStub(ch)
                getProject = await st.GetProject(GetProjectInput(id=id))
                return getProject
        except Exception as e:
            raise e

    async def get_projects(self, email: str):
        try:
            async with insecure_channel(self.url) as ch:
                st = InternalStub(ch)
                getProjects = await st.GetProjects(GetProjectsInput(email=email))
                return getProjects
        except Exception as e:
            raise e
    
    async def add_project(self, project: project_models.AddProjectInput):
        try:
            async with insecure_channel(self.url) as ch:
                st = InternalStub(ch)
                addProjectInput = AddProjectInput(**project) if type(project) is dict else AddProjectInput(**project.dict())
                addProject = await st.AddProject(addProjectInput)                 
                return addProject
        except Exception as e:
            raise e
    
    async def update_project(self, id: str, payload: UpdateProjectInputPayload):
        try:
            async with insecure_channel(self.url) as ch:
                st = InternalStub(ch)
                updateProject = await st.UpdateProject(UpdateProjectInput(id=id, updateProjectInputPayload=UpdateProjectInputPayload(**payload.dict())))
                return updateProject
        except Exception as e:
            raise e
    
    async def delete_project(self, id: str):
        try:
            async with insecure_channel(self.url) as ch:
                st = InternalStub(ch)
                deleteProject = await st.DeleteProject(DeleteProjectInput(id=id))
                return deleteProject
        except Exception as e:
            raise e
    
    async def watch_projects(self, email: str):
        try:
            async with insecure_channel(self.url) as ch:
                st = InternalStub(ch)
                async for project in st.WatchProjects(WatchProjectsInput(email=email)):
                    yield project
        except Exception as e:
            raise e

    def rpcError_exception_handler(_, request: Request, e: RpcError):
        if e.code() == StatusCode.INVALID_ARGUMENT:
            return JSONResponse(
                status_code=400,
                content=rest_exceptions.BadRequest().dict()
            )
        if e.code() == StatusCode.NOT_FOUND:
            return JSONResponse(
                status_code=404,
                content=rest_exceptions.NotFound(detail=e.details()).dict()
            )
        return JSONResponse(
            status_code=500,
            content=rest_exceptions.InternalServerError(
                detail=e.details(), debug=e.code()).dict()
        )