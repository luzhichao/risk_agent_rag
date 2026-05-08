# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026/5/8
"""
from datetime import datetime

from sqlalchemy import DateTime, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from core.snowflake import next_id


class BaseEntity(DeclarativeBase):
    """
    基础实体类
    @author: Luzhichao
    @date: 2026-05-08
    """
    id: Mapped[str] = mapped_column("id", String(64), primary_key=True, default=next_id,
                                    comment="实体ID")
    created_time: Mapped[datetime] = mapped_column("created_time", DateTime,
                                                   insert_default=datetime.now,
                                                   default=datetime.now,
                                                   comment="创建时间")
    updated_time: Mapped[datetime] = mapped_column("updated_time", DateTime,
                                                   insert_default=datetime.now,
                                                   onupdate=datetime.now,
                                                   default=datetime.now,
                                                   comment="更新时间")
