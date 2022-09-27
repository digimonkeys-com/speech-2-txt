from fastapi import HTTPException, status


class UserNotFound(HTTPException):
    def __init__(self, user_id: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id '{user_id}' not found."
        )


class ContentNotFound(HTTPException):
    def __init__(self, element_id: int, element: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{element.title()} with id '{element_id}' not found."
        )


class ProgressNotFound(HTTPException):
    def __init__(self, user_id: str, element_id: int, element: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{element.title()} '{element_id}' for User '{user_id}' not found."
        )


class CredentialsException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated.",
            headers={"WWW-Authenticate": "Bearer"}
        )
