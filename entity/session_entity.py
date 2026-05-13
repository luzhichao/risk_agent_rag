# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026-05-12
"""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from entity.base_entity import BaseEntity


class SessionEntity(BaseEntity):
    """
    用户会话数据实体
    @author: Luzhichao
    @date: 2026-05-12
    """
    __tablename__ = "t_session"

    user_id: Mapped[str] = mapped_column("user_id", String(64), nullable=False, comment="用户ID")
    session_name: Mapped[str] = mapped_column("session_name", String(255), nullable=False,
                                              comment="会话名称")
