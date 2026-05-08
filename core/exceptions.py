# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026/5/7
"""
from fastapi import status, FastAPI
from httpcore import Request

from core.response import error_response


class CustomException(Exception):
    """
    自定义异常
    :param
    :return
    @author: Luzhichao
    @date: 2026-05-08
    """

    def __init__(self, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
                 detail: str = "操作异常"):
        self.status_code = status_code
        self.detail = detail


# 全局异常处理器
def register_global_exception(app: FastAPI):
    # 捕获我们主动抛的 CustomException
    @app.exception_handler(CustomException)
    async def api_exception_handler(request: Request, exc: CustomException):
        return error_response(code=exc.status_code, msg=exc.detail)

    # 捕获所有未知异常（服务器500错误）
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        return error_response(msg=f"服务器异常：{str(exc)}")
