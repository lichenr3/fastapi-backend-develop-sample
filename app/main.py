from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.api_router import api_router
from app.utils.exception_handler import register_exception_handlers
from app.utils.logger_handler import setup_logging

setup_logging()  # 初始化日志配置

app = FastAPI(title="AI能力调用接口")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

register_exception_handlers(app)
app.include_router(api_router, prefix="/api/v1")

# uvicorn app.main:app --reload --host=0.0.0.0
