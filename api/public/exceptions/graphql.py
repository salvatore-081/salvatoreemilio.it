from graphql import GraphQLError


class NotFound(GraphQLError):
    def __init__(self, message: str):
        super().__init__(message=message)


class InvalidArgument(GraphQLError):
    def __init__(self, key: str):
        super().__init__(message=f"'{key}' input can not be empty")


class InternalServerError(GraphQLError):
    def __init__(self, message: str):
        super().__init__(message=f"{message}")


class Unauthorized(GraphQLError):
    def __init__(self):
        super().__init__(message="invalid credentials")


class BadRequest(GraphQLError):
    def __init__(self, message: str):
        super().__init__(message=message)


class Forbidden(GraphQLError):
    def __init__(self) -> None:
        super().__init__("forbidden")
