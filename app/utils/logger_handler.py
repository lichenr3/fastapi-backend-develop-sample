
import sys
import logging
from datetime import datetime
from sqlalchemy import insert
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.core.db_session import SessionLocal


# class DatabaseLogHandler(logging.Handler):
#     def __init__(self, db_session_factory: sessionmaker):
#         """
#         db_session_factory: 传入 SessionLocal 工厂
#         """
#         super().__init__()
#         self.db_session_factory = db_session_factory

#     def emit(self, record: logging.LogRecord):
#         """
#         当日志被处理时，这个方法会被 logging 模块自动调用。
#         `record` 对象包含了所有日志信息。
#         """
#         db = self.db_session_factory()
#         try:
#             stmt = insert(ai_model_logs).values(
#                 logs_info=self.format(record),
#                 log_type=2,
#                 create_time=datetime.now()  # 创建时间
#             )
#             db.execute(stmt)
#             db.commit()
#         except Exception:
#             db.rollback()
#             self.handleError(record) # 调用基类方法处理错误
#         finally:
#             db.close()


def setup_logging():
    # 获取根 logger
    root_logger = logging.getLogger()

    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)
    root_logger.setLevel(log_level)

    # 清除所有已存在的 handlers，避免重复输出
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    formatter = logging.Formatter('[%(levelname)s] %(asctime)s %(name)s: %(message)s')

    # 1. 控制台 Handler
    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setFormatter(formatter)
    root_logger.addHandler(ch)

    # 2. 数据库 Handler (只在生产环境启用)
    # if settings.app_env == 'prod':
    #     db_handler = DatabaseLogHandler(db_session_factory=SessionLocal)
    #     db_handler.setLevel(logging.INFO) # 只记录 INFO 及以上级别到数据库
    #     db_handler.setFormatter(formatter)
    #     root_logger.addHandler(db_handler)

    # 为特定库设置日志级别，避免过多噪音
    logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
