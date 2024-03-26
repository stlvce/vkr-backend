from fastapi import HTTPException

from typing import Optional, Dict


class DetailedHTTPException(HTTPException):
    STATUS_CODE: int
    DETAIL: str
    HEADERS: Optional[Dict[str, str]] | None = None

    def __init__(self) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, headers=self.HEADERS)


class UnauthorizedException(DetailedHTTPException):
    STATUS_CODE = 401
    DETAIL = "Could not validate credentials"
    HEADERS = {"WWW-Authenticate": "Bearer"}
