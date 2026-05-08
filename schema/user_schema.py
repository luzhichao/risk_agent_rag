#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026-05-08
"""
import re

from pydantic import BaseModel, EmailStr, field_validator


class UserRegister(BaseModel):
    """
    用户注册类
    @author: Luzhichao
    @date: 2026-05-08
    """
    user_name: str
    phone: str
    email: EmailStr
    user_password: str

    @field_validator("user_name")
    def validate_username(cls, v):
        v = v.strip()
        # 不能为空
        if not v:
            raise ValueError("用户名不能为空")
        # 不能超过10位
        if len(v) > 10:
            raise ValueError("用户名长度不能超过10位")
        # 只能是英文字母
        if not re.match(r'^[a-zA-Z]+$', v):
            raise ValueError("用户名只能包含英文字母")
        return v

    @field_validator("phone")
    def validate_phone(cls, v):
        if not re.match(r"^1[3-9]\d{9}$", v):
            raise ValueError("手机号格式不正确")
        return v

    @field_validator("user_password")
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("密码长度不能少于6位")
        return v


class UserLogIn(BaseModel):
    """
    用户登录类
    @author: Luzhichao
    @date: 2026-05-08
    """
    user_name: str
    user_password: str

    @field_validator("user_name")
    def validate_username(cls, v):
        v = v.strip()
        # 不能为空
        if not v:
            raise ValueError("用户名不能为空")
        # 不能超过10位
        if len(v) > 10:
            raise ValueError("用户名长度不能超过10位")
        # 只能是英文字母
        if not re.match(r'^[a-zA-Z]+$', v):
            raise ValueError("用户名只能包含英文字母")
        return v

    @field_validator("user_password")
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError("密码长度不能少于6位")
        return v


class Token(BaseModel):
    """
    登录token对象
    @author: Luzhichao
    @date: 2026-05-08
    """
    user_id: int = None
    user_name: str = None
