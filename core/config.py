# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026/5/7
"""
import os
from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    # 服务配置
    api_version: str = Field(default=os.getenv("API_VERSION", "v1"))
    secret_key: str = Field(default=os.getenv("SECRET_KEY"))
    algorithm: str = Field(default=os.getenv("ALGORITHM", "HS256"))
    access_token_expire_minutes: int = Field(default=os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

    # 系统提示词路径
    system_prompt_file_path: str = Field(
        default=os.getenv("SYSTEM_PROMPT_FILE_PATH",
                          f"{Path(__file__).parent.parent}/prompt/system_prompt.md"))

    # 通义大模型配置
    base_url: str = Field(
        default=os.getenv("BASE_URL", "https://dashscope.aliyuncs.com/compatible-mode/v1"))
    dashscope_api_key: str = Field(default=os.getenv("DASHSCOPE_API_KEY", ""))
    multimodal_model_name: str = Field(default=os.getenv("MULTIMODAL_MODEL_NAME", "qwen3.6-plus"))
    text_model_name: str = Field(default=os.getenv("TEXT_MODEL_NAME", "qwen3.5-35b-a3b"))
    embedding_model_name: str = Field(
        default=os.getenv("EMBEDDING_MODEL_NAME", "text-embedding-v4"))

    # Chroma配置
    chroma_persist_directory: str = Field(
        default=os.getenv("CHROMA_PERSIST_DIRECTORY", "./db/chroma_db"))
    chroma_collection_name: str = Field(
        default=os.getenv("CHROMA_COLLECTION_NAME", "risk_agent_rag"))
    # tavily配置
    tavily_api_key: str = Field(default=os.getenv("TAVILY_API_KEY", ""))

    # 文本分块配置
    chunk_size: int = 500
    chunk_overlap: int = 50

    # OCR配置
    # baidu_ocr_app_id: str = Field(default=os.getenv("BAIDU_OCR_APP_ID"))
    # baidu_ocr_api_key: str = Field(default=os.getenv("BAIDU_OCR_API_KEY"))
    # baidu_ocr_secret_key: str = Field(default=os.getenv("BAIDU_OCR_SECRET_KEY"))

    # 数据库配置
    mysql_driver: str = Field(default="mysql+aiomysql")
    mysql_db_user: str = Field(default=os.getenv("MYSQL_DB_USER", "root"))
    mysql_db_password: str = Field(default=os.getenv("MYSQL_DB_PASSWORD", "123456"))
    mysql_db_host: str = Field(default=os.getenv("MYSQL_DB_HOST", "127.0.0.1"))
    mysql_db_port: int = Field(default=os.getenv("MYSQL_DB_PORT", 3306))
    mysql_db_database: str = Field(default=os.getenv("MYSQL_DB_DATABASE", "safety_risk"))

    # redis 配置
    redis_host: str = Field(default=os.getenv("REDIS_HOST", "127.0.0.1"))
    redis_port: int = Field(default=os.getenv("REDIS_PORT", 6379))
    redis_password: str = Field(default=os.getenv("REDIS_PASSWORD", ""))

    @property
    def mysql_database_url(self) -> str:
        return f"{self.mysql_driver}://{self.mysql_db_user}:{self.mysql_db_password}@{self.mysql_db_host}:{self.mysql_db_port}/{self.mysql_db_database}"

    model_config = SettingsConfigDict(
        case_sensitive=False,  # 不区分大小写
        env_file=".env",  # 自动加载 .env 文件
        env_ignore_empty=True  # 忽略空环境变量
    )


# 全局配置实例
settings = Settings()
