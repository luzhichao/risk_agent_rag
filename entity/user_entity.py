# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026/5/8
"""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from entity.base_entity import BaseEntity


class UserEntity(BaseEntity):
    """
    用户数据实体
    @author: Luzhichao
    @date: 2026-05-08
    """
    __tablename__ = "t_user"
    user_name: Mapped[str] = mapped_column("user_name", String(64), nullable=False,
                                           comment="用户名")
    user_password: Mapped[str] = mapped_column("password", String(255), nullable=False,
                                               comment="用户密码")
    email: Mapped[str] = mapped_column("email", String(64), nullable=False,
                                       comment="用户邮箱")
    phone: Mapped[str] = mapped_column("phone", String(64), nullable=False,
                                       comment="用户手机")
