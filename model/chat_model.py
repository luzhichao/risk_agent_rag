#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026/5/7
"""
from pydantic import BaseModel, Field


class ChatResponse(BaseModel):
    """
    智能回复数据模型
    """
    name: str = Field(description="隐患名称")
    source: str = Field(description="隐患来源")
    description: str = Field(description="隐患描述")
    according: str = Field(description="隐患依据")
    solution: str = Field(description="隐患解决方案")
    risk_type: str = Field(description="隐患类型")
    risk_level: str = Field(description="隐患等级")
    risk_status: str = Field(description="隐患状态")
