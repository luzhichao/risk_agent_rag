# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026/5/8
"""
from typing import Optional, AsyncGenerator

from utils.llm_utils import chat


class ChatService:

    @staticmethod
    async def ask_chat(session_id: str, question: str,
                       image_urls: Optional[list[str]] = None
                       ) -> AsyncGenerator[str, None]:
        """
        用户提问方法
        :param
        :return
        @author: Luzhichao
        @date: 2026-05-08
        """
        # TODO 可完善根据用户ID和session id判断是否存在会话
        return chat(text=question, session_id=session_id, images=image_urls)
