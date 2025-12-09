"""
自定义异常和异常处理器
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlalchemy.exc import SQLAlchemyError


class APIException(Exception):
    """
    自定义API异常类
    """
    def __init__(self, status_code: int, detail: str, error_code: str = "UNKNOWN_ERROR"):
        self.status_code = status_code
        self.detail = detail
        self.error_code = error_code
        super().__init__(self.detail)


class NotFoundError(APIException):
    """
    资源未找到异常
    """
    def __init__(self, detail: str, error_code: str = "NOT_FOUND"):
        super().__init__(status.HTTP_404_NOT_FOUND, detail, error_code)


class BadRequestError(APIException):
    """
    请求参数错误异常
    """
    def __init__(self, detail: str, error_code: str = "BAD_REQUEST"):
        super().__init__(status.HTTP_400_BAD_REQUEST, detail, error_code)


class UnauthorizedError(APIException):
    """
    未授权异常
    """
    def __init__(self, detail: str, error_code: str = "UNAUTHORIZED"):
        super().__init__(status.HTTP_401_UNAUTHORIZED, detail, error_code)


class ForbiddenError(APIException):
    """
    禁止访问异常
    """
    def __init__(self, detail: str, error_code: str = "FORBIDDEN"):
        super().__init__(status.HTTP_403_FORBIDDEN, detail, error_code)


class InternalServerError(APIException):
    """
    内部服务器错误异常
    """
    def __init__(self, detail: str, error_code: str = "INTERNAL_SERVER_ERROR"):
        super().__init__(status.HTTP_500_INTERNAL_SERVER_ERROR, detail, error_code)


async def http_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    """
    自定义HTTP异常处理器
    """
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "code": exc.error_code,
            "message": exc.detail,
            "data": None
        },
    )


async def validation_exception_handler(request: Request, exc: ValidationError) -> JSONResponse:
    """
    Pydantic验证异常处理器
    """
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "code": "VALIDATION_ERROR",
            "message": "请求参数验证失败",
            "data": {
                "errors": exc.errors()
            }
        },
    )


async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError) -> JSONResponse:
    """
    SQLAlchemy数据库异常处理器
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": "DATABASE_ERROR",
            "message": "数据库操作失败",
            "data": None
        },
    )


async def generic_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """
    通用异常处理器
    """
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "code": "INTERNAL_SERVER_ERROR",
            "message": "服务器内部错误",
            "data": None
        },
    )


def setup_exception_handlers(app: FastAPI) -> None:
    """
    设置异常处理器
    
    Args:
        app: FastAPI应用实例
    """
    # 注册自定义异常处理器
    app.add_exception_handler(APIException, http_exception_handler)
    
    # 注册Pydantic验证异常处理器
    app.add_exception_handler(ValidationError, validation_exception_handler)
    
    # 注册SQLAlchemy数据库异常处理器
    app.add_exception_handler(SQLAlchemyError, sqlalchemy_exception_handler)
    
    # 注册通用异常处理器
    app.add_exception_handler(Exception, generic_exception_handler)