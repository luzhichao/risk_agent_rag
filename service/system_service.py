#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026-05-08
"""
import logging

from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import CustomException
from core.security import create_access_token
from entity.user_entity import UserEntity
from schema.user_schema import UserRegister, UserLogIn

logger = logging.getLogger("system_api")
pwd_context = CryptContext(schemes=["argon2"], deprecated="auto")


async def _check_user(db: AsyncSession, record):
    """
    检查用户信息
    :param
    :return
    @author: Luzhichao
    @date: 2026-05-08
    """
    result = await db.execute(select(UserEntity).filter(record))
    return result.scalar_one_or_none()


class UserService:
    @staticmethod
    async def register(db: AsyncSession, user: UserRegister):
        # 检查用户名是否存在
        if await _check_user(db, UserEntity.user_name == user.user_name):
            raise CustomException(detail="用户名已存在")
        if await _check_user(db, UserEntity.phone == user.phone):
            raise CustomException(detail="手机号已被注册")
        if await _check_user(db, UserEntity.email == user.email):
            raise CustomException(detail="邮箱已被注册")

        # 密码加密
        hashed_pwd = pwd_context.hash(user.user_password)

        db_user = UserEntity(
            user_name=user.user_name,
            phone=user.phone,
            email=user.email,
            user_password=hashed_pwd
        )

        try:
            db.add(db_user)
            await db.commit()
            await db.refresh(db_user)
        except Exception as e:
            logger.error(e)
            await db.rollback()
            raise Exception("注册失败")

    @staticmethod
    async def login(db: AsyncSession, user: UserLogIn):
        """
        用户登录
        :param
        :return
        @author: Luzhichao
        @date: 2026-05-08
        """
        db_user: UserEntity | None = await _check_user(db, UserEntity.user_name == user.user_name)
        if not db_user:
            raise CustomException(detail="用户不存在")
        if not pwd_context.verify(user.user_password, db_user.user_password):
            raise CustomException(detail="账号或密码错误")

        try:
            token = create_access_token(db_user.id, db_user.user_name)
            return token
        except Exception as e:
            logger.error(e)
            raise Exception("登录失败")
