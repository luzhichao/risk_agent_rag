#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026-05-12
"""
from pydantic import BaseModel, Field


class Knowledge(BaseModel):
    """
    知识数据验证对象
    :param
    :return
    @author: Luzhichao
    @date: 2026-05-12
    """
    knowledge_name: str = Field(..., min_length=2, max_length=50, description="知识标题")
    type: str = Field(..., min_length=2, max_length=20, description="知识类型")
    status: str = Field(default="unfinished", min_length=2, max_length=20, description="知识状态")
    path: str = Field(..., min_length=2, max_length=100, description="知识路径")
    url: str = Field(..., min_length=2, max_length=100, description="知识URL")
