class Forbidden(Exception):
    def __init__(self) -> None:
        super().__init__('forbidden')


class BadRequest(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)


class Unauthorized(Exception):
    def __init__(self) -> None:
        super().__init__('unauthorized')
