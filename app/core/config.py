
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    应用配置类
    用于加载环境变量和配置项
    """
    # 应用环境配置
    app_env: str = "prod"
    log_level: str = "INFO"
    server_host: str = "0.0.0.0"
    server_port: int = 8000

    # MySQL 数据库配置
    mysql_host: str
    mysql_port: int
    mysql_user: str
    mysql_password: str
    mysql_database: str

    # dev 环境变量
    mysql_user_dev: str = ""

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    def __init__(self, **values):
        super().__init__(**values)
        # dev 环境自动切换
        if self.app_env == "dev" and self.mysql_user_dev:
            self.mysql_user = self.mysql_user_dev


settings = Settings()
