# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026/5/7
"""
from typing import Any, Optional

from fastapi import status
from pydantic import BaseModel


class Result(BaseModel):
    """
    统一返回对象
    :param
    :return
    @author: Luzhichao
    @date: 2026-05-09
    """
    status_code: int = status.HTTP_200_OK
    msg: str = "操作成功"
    data: Optional[Any] = None

    # model_config = ConfigDict(arbitrary_types_allowed=True)

    @staticmethod
    def success(data: Any = None, msg: str = "操作成功") -> "Result":
        """
        操作成功
        @author: Luzhichao
        @date: 2026-05-07
        """
        return Result(msg=msg, data=data)

    @staticmethod
    def error(code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, msg: str = "操作失败",
              data: Any = None) -> "Result":
        """
        操作异常
        @author: Luzhichao
        @date: 2026-05-07
        """
        return Result(status_code=code, msg=msg, data=data)
