# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026/5/7
"""
import logging
import os
from datetime import datetime
from logging.handlers import RotatingFileHandler

import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, status
from httpcore import Request
from langgraph_sdk.auth.exceptions import HTTPException

from api.chat import router as chat_router
from api.knowledge_base import router as knowledge_router
from api.risk_identify import router as risk_router
from api.session import router as session_router
from core.config import settings
from entity.base_entity import BaseEntity
from utils.db_utils import engine

# 加载环境变量
load_dotenv()

logger = logging.getLogger("main")


# 配置日志
def setup_logging():
    log_dir = "logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    log_file = os.path.join(log_dir, "safety_risk_agent.log")

    # 日志格式
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # 旋转日志（最大50MB，保留5个备份）
    file_handler = RotatingFileHandler(
        log_file, maxBytes=50 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # 控制台输出
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # 全局日志配置
    logging.basicConfig(
        level=logging.INFO,
        handlers=[file_handler, console_handler]
    )


def create_app() -> FastAPI:
    """创建FastAPI应用"""
    app = FastAPI(
        title="安全隐患识别智能问答服务",
        description="基于LangChain+通义大模型的安全隐患识别智能问答服务",
        version=settings.api_version
    )

    # 注册路由
    app.include_router(risk_router)
    app.include_router(knowledge_router)
    app.include_router(session_router)
    app.include_router(chat_router)

    # 健康检查接口
    @app.get("/health", tags=["健康检查"])
    async def health_check():
        return {"status": "healthy", "version": settings.api_version}

    @app.get("/", tags=[""])
    async def root():
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Not Found")

    @app.middleware("http")
    async def log_request(request: Request, call_next):
        """请求日志中间件"""
        start_time = datetime.now()
        response = await call_next(request)
        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds() * 1000
        logger.info(f"{request.method} {request.url} {response.status_code} {duration:.2f}ms")
        return response

    # 启动时创建表
    @app.on_event("startup")
    async def startup():
        async with engine.begin() as conn:
            await conn.run_sync(BaseEntity.metadata.create_all)

    logger.info("安全隐患识别智能问答服务初始化完成")
    return app


if __name__ == "__main__":
    setup_logging()
    logger.info("启动安全隐患识别智能问答服务...")

    # 启动FastAPI服务
    uvicorn.run(
        "main:create_app",
        host=os.getenv("SERVER_HOST", "127.0.0.1"),
        port=int(os.getenv("SERVER_PORT", 8000)),
        reload=True,  # 开发环境开启，生产环境关闭
        factory=True
    )
