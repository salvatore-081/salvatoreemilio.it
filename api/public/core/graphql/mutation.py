from ariadne import MutationType
from state.appState import AppState


def getQuery(appState: AppState) -> MutationType:
    query = MutationType()

    @query.field("addUser")
    async def resolve_getUser(_, info, email):
        return
