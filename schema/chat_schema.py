#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026-05-09
"""
from pydantic import BaseModel, Field


class Ask(BaseModel):
    question: str = Field(..., min_length=2, max_length=200, description="用户提问内容")
    image_urls: list[str] = Field([], max_length=5, description="用户上传的图片URL地址列表，最多5张")
    session_id: str = Field(None, description="会话ID，没有则会自动创建新会话")
