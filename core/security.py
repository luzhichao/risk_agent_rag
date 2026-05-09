# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026/5/7
"""
from datetime import timedelta

from fastapi import status, Header
from jose import JWTError, jwt

from core.exceptions import CustomException
from schema.user_schema import Token
from utils import time_utils

# token配置
SECRET_KEY = "i&a~=QSk2Hs_nGM!.9e3RVOWf),:6Yv5#hP}x{ow<rTl@q>puyUd]^EDA/+*|8"
ALGORITHM = "HS256"
# 7天(60 * 24 * 7)
ACCESS_TOKEN_EXPIRE_MINUTES = 1


def create_access_token(user_id: int, user_name: str) -> str:
    """
    创建token
    :param
    :return
    @author: Luzhichao
    @date: 2026-05-08
    """
    expire = time_utils.add_time(timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode = {
        "user_id": user_id,
        "user_name": user_name,
        "exp": expire
    }
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_token(token: str = Header(default=None, alias="Authorization")):
    """
    校验登录token
    :param
    :return
    @author: Luzhichao
    @date: 2026-05-08
    """
    if token is None:
        raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED,
                              detail="登录失效，请重新登录")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM],
                             options={"verify_exp": True})
        user_id: int = payload.get("user_id")
        user_name: str = payload.get("user_name")
        if user_id is None:
            raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED,
                                  detail="登录失效，请重新登录")
        return Token(user_id=user_id, user_name=user_name)
    except JWTError:
        raise CustomException(status_code=status.HTTP_401_UNAUTHORIZED,
                              detail="登录失效，请重新登录")
