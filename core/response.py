# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026/5/7
"""
from typing import Any

from fastapi import status
from fastapi.responses import JSONResponse


def success_response(data: Any = None, msg: str = "操作成功") -> JSONResponse:
    """
    操作成功
    @author: Luzhichao
    @date: 2026-05-07
    """
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": status.HTTP_200_OK,
            "msg": msg,
            "data": data
        }
    )


def error_response(code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, msg: str = "操作失败",
                   data: Any = None) -> JSONResponse:
    """
    操作异常
    @author: Luzhichao
    @date: 2026-05-07
    """
    return JSONResponse(
        status_code=code,
        content={
            "code": code,
            "msg": msg,
            "data": data
        }
    )
