# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026/5/7
"""
from fastapi import HTTPException, status


# ======================
# 自定义异常
# ======================
class FileProcessError(HTTPException):
    """文件处理异常"""

    def __init__(self, detail: str = "文件处理失败"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )


class TimeProcessError(HTTPException):
    """时间处理异常"""

    def __init__(self, detail: str = "时间处理失败"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )


class ModelCallError(HTTPException):
    """大模型调用异常"""

    def __init__(self, detail: str = "大模型调用失败"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )


class KnowledgeBaseError(HTTPException):
    """知识库操作异常"""

    def __init__(self, detail: str = "知识库操作失败"):
        super().__init__(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=detail
        )


class SessionError(HTTPException):
    """会话操作异常"""

    def __init__(self, detail: str = "会话操作失败"):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail
        )
