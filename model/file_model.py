#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026-05-12
"""
from pydantic import BaseModel, Field


class FileResponse(BaseModel):
    """
    文件数据返回响应对象
    @author: Luzhichao
    @date: 2026-05-12
    """
    file_name: str = Field(description="文件名称")
    path: str = Field(description="文件路径")
    url: str = Field(description="可访问URL")
    type: str = Field(description="文件类型")
