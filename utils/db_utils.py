# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026/5/7
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, AsyncEngine
from sqlalchemy.orm import sessionmaker

from core.config import settings

engine: AsyncEngine = create_async_engine(url=settings.mysql_database_url, echo=True, pool_size=10,
                                          # pool_pre_ping=True,
                                          # pool_recycle=3600,
                                          max_overflow=20)

AsyncSessionLocal: AsyncSession = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    autoflush=False,
    expire_on_commit=False,
    autocommit=False,
)


async def get_db():
    async with AsyncSessionLocal as session:
        try:
            yield session
        finally:
            await session.close()
