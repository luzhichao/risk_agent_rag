# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026/5/7
"""
import logging

from fastapi import APIRouter, Body, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession

from core.config import settings
from core.response import Result
from core.security import verify_token
from schema.chat_schema import Ask
from schema.user_schema import Token
from service.chat_service import ChatService
from utils.db_utils import get_db

logger = logging.getLogger("chat_api")

router = APIRouter(prefix=f"/api/{settings.api_version}/chat", tags=["智能问答接口"])


@router.post(path="/ask", summary="智能问答", description="安全问题智能问答")
async def ask_question(
        ask: Ask = Body(..., description="用户提问信息"),
        user: Token = Depends(verify_token),
        db: AsyncSession = Depends(get_db),
):
    """
    用户提问接口（核心智能问答入口）
    1. 接收用户问题
    2. 查询知识库
    3. 调用大模型
    4. 返回回答
    5. 保存对话历史
    :param
    :return
    @author: Luzhichao
    @date: 2026-05-07
    """
    try:
        answer = await ChatService.ask_chat(
            session_id=ask.session_id,
            user_id=user.user_id,
            question=ask.question,
            image_urls=ask.image_urls,
            db=db
        )
        return StreamingResponse(
            content=answer,
            media_type="application/json; charset=utf-8"
        )
    except Exception as e:
        logger.error(f"用户提问异常：{str(e)}")
        return Result.error(msg="服务器繁忙，请稍后再试")
