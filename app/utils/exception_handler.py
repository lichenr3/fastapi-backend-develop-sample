
import logging
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger(__name__)


# 自定义异常类
class BusinessException(Exception):
    """业务逻辑异常"""
    def __init__(self, message: str, error_code: str = "BUSINESS_ERROR", status_code: int = 500):
        self.message = message
        self.error_code = error_code
        self.status_code = status_code
        super().__init__(message, error_code, status_code)


class DataValidationException(BusinessException):
    """数据验证异常"""
    def __init__(self, message: str, error_code: str = "VALIDATION_ERROR"):
        super().__init__(message, error_code, 500)


class DatabaseException(BusinessException):
    """数据库操作异常"""
    def __init__(self, message: str, error_code: str = "DATABASE_ERROR"):
        super().__init__(message, error_code, 500)


class LLMAPIException(BusinessException):
    """LLM API 调用异常"""
    def __init__(self, message: str, error_code: str = "LLM_API_ERROR"):
        super().__init__(message, error_code, 500)


class FeatureExtractionException(BusinessException):
    """人脸特征提取专用异常"""
    def __init__(self, message: str, error_code: str = "FEATURE_EXTRACT_ERROR"):
        super().__init__(message, error_code, 500)


class ImagePathValidationException(BusinessException):
    """人脸库本地上传专用异常"""
    def __init__(self, message: str, error_code: str = "FACE_PATH_ERROR"):
        super().__init__(message, error_code, 500)


# 全局异常处理注册函数
def register_exception_handlers(app):
    """全局异常处理注册"""

    @app.exception_handler(BusinessException)
    async def business_exception_handler(request: Request, exc: BusinessException):
        logger.error(f"业务异常", extra={
            "path": request.url.path,
            "method": request.method
        })
        logger.debug(f"异常信息: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.status_code,
                "message": exc.message
            }
        )

    @app.exception_handler(DataValidationException)
    async def data_validation_exception_handler(request: Request, exc: DataValidationException):
        logger.error(f"数据验证异常", extra={
            "path": request.url.path,
            "method": request.method
        })
        logger.debug(f"异常信息: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.status_code,
                "message": exc.message
            }
        )

    @app.exception_handler(DatabaseException)
    async def database_exception_handler(request: Request, exc: DatabaseException):
        logger.error(f"数据库异常", extra={
            "path": request.url.path,
            "method": request.method
        })
        logger.debug(f"异常信息: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.status_code,
                "message": "数据操作失败" # 自定义错误信息, 避免数据泄露
            }
        )

    @app.exception_handler(LLMAPIException)
    async def llm_api_exception_handler(request: Request, exc: LLMAPIException):
        logger.error(f"LLM API异常", extra={
            "path": request.url.path,
            "method": request.method
        })
        logger.debug(f"异常信息: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.status_code,
                "message": "LLM API调用失败"
            }
        )

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(request: Request, exc: StarletteHTTPException):
        logger.error(f"HTTP异常", extra={
            "path": request.url.path,
            "method": request.method
        })
        logger.debug(f"异常信息: {exc.detail}")
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "code": exc.status_code,
                "message": exc.detail if isinstance(exc.detail, str) else "后端系统错误"
            },
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        logger.error(f"未知异常", extra={
            "path": request.url.path,
            "method": request.method
        })
        logger.debug(f"异常信息: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={
                "code": 500,
                "message": "后端系统错误"
            },
        )
