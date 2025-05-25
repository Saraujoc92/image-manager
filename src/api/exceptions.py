from fastapi import HTTPException


class AuthorizationError(HTTPException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(status_code=403, detail=message)

class NotFoundError(HTTPException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(status_code=404, detail=message)

class BadRequestError(HTTPException):
    def __init__(self, message: str = "Bad request"):
        super().__init__(status_code=400, detail=message)