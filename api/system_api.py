#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026-05-08
"""
import logging

from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.response import Result
from core.security import verify_token
from schema.user_schema import UserRegister, UserLogIn, Token
from service.system_service import UserService
from utils.db_utils import get_db

logger = logging.getLogger("system_api")

router = APIRouter(prefix=f"/api/{settings.api_version}/system", tags=["系统管理接口"])


@router.post(path="/register", summary="用户注册", description="用户注册接口")
async def register(
        user: UserRegister = Body(..., description="用户注册信息"),
        db: AsyncSession = Depends(get_db)
):
    """
    用户注册接口
    :param
    :return
    @author: Luzhichao
    @date: 2026-05-08
    """
    await UserService.register(db, user)
    return Result.success(data=True, msg="注册成功")


@router.post(path="/login", summary="用户登录", description="用户登录接口")
async def login(
        user: UserLogIn = Body(..., description="用户登录信息"),
        db: AsyncSession = Depends(get_db)
):
    """
    用户注册接口
    :param
    :return
    @author: Luzhichao
    @date: 2026-05-08
    """
    token = await UserService.login(db, user)
    return Result.success(data=token, msg="登录成功")


@router.post(path="/get_user_info", summary="登录用户信息", description="获取登录用户信息")
async def get_user_info(
        user: Token = Depends(verify_token),
):
    """
    获取登录用户信息
    :param
    :return
    @author: Luzhichao
    @date: 2026-05-09
    """

    return Result.success(data=user, msg="操作成功")
