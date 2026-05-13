#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026-05-12
"""
from pydantic import BaseModel, Field


class KnowledgeResponse(BaseModel):
    """
    知识库数据返回响应对象
    @author: Luzhichao
    @date: 2026-05-12
    """
    doc_id: str = Field(description="文档ID")
    knowledge_name: str = Field(description="知识名称")
    type: str = Field(description="知识类型")
    status: str = Field(description="知识状态")
    path: str = Field(description="知识路径")
    url: str = Field(description="可访问URL")
