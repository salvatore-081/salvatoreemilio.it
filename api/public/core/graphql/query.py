from ariadne import QueryType

from state.appState import AppState


def getQuery(appState: AppState) -> QueryType:
    query = QueryType()

    @query.field("getUser")
    async def resolve_getUser(_, info, email):
        return await appState.gqlClient.get_user(email)

    return query
