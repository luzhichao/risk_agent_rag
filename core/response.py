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
    """成功响应"""
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
    """错误响应"""
    return JSONResponse(
        status_code=code,
        content={
            "code": code,
            "msg": msg,
            "data": data
        }
    )


# 隐患识别专用响应
def risk_identify_response(
        risk_status: str,
        risk_total: int,
        risk_list: list,
        cost_time: str,
        msg: str
) -> JSONResponse:
    """隐患识别结果响应"""
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            "code": status.HTTP_200_OK,
            "msg": "识别完成",
            "data": {
                "status": risk_status,
                "riskTotal": risk_total,
                "riskList": risk_list,
                "costTime": cost_time,
                "msg": msg
            }
        }
    )
