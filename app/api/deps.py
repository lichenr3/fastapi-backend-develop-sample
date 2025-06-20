
from app.core.db_session import get_db_session


def get_db():
    yield from get_db_session() # 转发数据库会话
