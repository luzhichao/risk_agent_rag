#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026-05-09
"""
from pydantic import BaseModel, Field


class SessionResponse(BaseModel):
    """
    session响应对象
    @author: Luzhichao
    @date: 2026-05-09
    """
    session_id: str = Field(description="会话ID")
    session_name: str = Field(description="会话名称")
    user_id: str = Field(description="用户ID")


class SessionHistoryResponse(BaseModel):
    """
    会话历史响应对象
    @author: Luzhichao
    @date: 2026-05-09
    """
    type: str = Field(description="会话类型")
    content: str | list[str | dict] = Field(description="会话内容")
