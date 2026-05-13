# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026/5/8
"""
from typing import Optional, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import CustomException
from service.session_service import SessionService
from utils.llm_utils import chat


class ChatService:
    """
    问答服务
    @author: Luzhichao
    @date: 2026-05-12
    """

    @staticmethod
    async def ask_chat(session_id: str, question: str,
                       user_id: str,
                       db: AsyncSession,
                       image_urls: Optional[list[str]] = None
                       ) -> AsyncGenerator[str, None]:
        """
        用户提问方法
        :param
        :return
        @author: Luzhichao
        @date: 2026-05-08
        """
        # 根据用户ID和会话ID判断是否存在会话
        if session_id is None:
            raise CustomException(detail="会话不存在")
        else:
            # 获取用户会话信息
            session = await SessionService.get_user_sessions(db=db, user_id=user_id,
                                                             session_id=session_id)
            if session is None:
                # 会话不存在
                raise CustomException(detail="会话不存在")

        return chat(text=question, session_id=session_id, images=image_urls)
