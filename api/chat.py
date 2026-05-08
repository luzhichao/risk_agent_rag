# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026/5/7
"""
import logging

from fastapi import APIRouter, Body
from fastapi.responses import StreamingResponse

from core.config import settings
from core.response import error_response
from service.chat_service import ChatService

logger = logging.getLogger("chat_api")

router = APIRouter(prefix=f"/api/{settings.api_version}/chat", tags=["智能问答接口"])


@router.post("/ask")
async def ask_question(
        question: str = Body(..., description="用户提问内容"),
        image_urls: list[str] = Body([], description="图片URL列表"),
        session_id: str = Body(..., description="会话ID，必须先创建"),
        # user_id: str = Depends(verify_token)
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
            session_id=session_id,
            question=question,
            image_urls=image_urls
        )
        return StreamingResponse(
            content=answer,
            media_type="application/json; charset=utf-8"
        )
    except Exception as e:
        logger.error(f"用户提问异常：{str(e)}")
        return error_response(msg="服务器繁忙，请稍后再试")
