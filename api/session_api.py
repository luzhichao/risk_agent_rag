# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026/5/9
"""
import logging

from fastapi import APIRouter, Depends, Body
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.response import Result
from core.security import verify_token
from schema.user_schema import Token
from service.session_service import SessionService
from utils.db_utils import get_db

logger = logging.getLogger("session_api")

router = APIRouter(prefix=f"/api/{settings.api_version}/session", tags=["会话历史管理接口"])


@router.post(path="/create", summary="用户创建新会话", description="用户创建新会话")
async def create_session(
        session_name: str = Body("未命名会话", min_length=2, max_length=20, description="会话名称"),
        user: Token = Depends(verify_token),
        db: AsyncSession = Depends(get_db),
):
    """
    用户创建新会话
    @author: Luzhichao
    @date: 2026-05-09
    """
    session_id = await SessionService.create_new_session(db, user.user_id, session_name)
    return Result.success(data=session_id, msg="会话创建成功")


@router.post(path="/update", summary="用户修改会话标题", description="用户修改会话标题")
async def update_session(
        session_id: str = Body(..., description="会话ID"),
        session_name: str = Body(..., min_length=2, max_length=20, description="会话名称"),
        user: Token = Depends(verify_token),
        db: AsyncSession = Depends(get_db),
):
    """
    用户创建新会话
    @author: Luzhichao
    @date: 2026-05-10
    """
    session_id = await SessionService.update_session(db, user.user_id, session_id, session_name)
    return Result.success(data=session_id, msg="会话创建成功")


@router.post(path="/list_user_sessions", summary="获取用户会话列表", description="获取用户会话列表")
async def list_user_sessions(
        db: AsyncSession = Depends(get_db),
        user: Token = Depends(verify_token)
):
    """
    获取用户会话列表
    @author: Luzhichao
    @date: 2026-05-07
    """
    sessions = await SessionService.list_user_sessions(db=db, user_id=user.user_id)
    return Result.success(data=sessions, msg="查询成功")


@router.post(path="/session_history", summary="指定会话历史查询", description="指定会话历史查询")
async def session_history(
        session_id: str = Body(..., description="会话ID"),
        db: AsyncSession = Depends(get_db),
        user: Token = Depends(verify_token)
):
    """
    指定会话历史查询
    @author: Luzhichao
    @date: 2026-05-07
    """
    result = await SessionService.session_history(session_id=session_id, user_id=user.user_id,
                                                  db=db)
    return Result.success(data=result, msg="查询成功")


@router.post(path="/clear_session_history", summary="会话历史清空", description="会话历史清空")
async def clear_session_history(
        session_id: str = Body(..., description="会话ID"),
        db: AsyncSession = Depends(get_db),
        user: Token = Depends(verify_token)
):
    """
    会话记忆清空
    @author: Luzhichao
    @date: 2026-05-07
    """
    await SessionService.clear_session_history(session_id=session_id, user_id=user.user_id, db=db)
    return Result.success(msg="清空成功")
