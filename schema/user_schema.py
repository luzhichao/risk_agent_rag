#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026-05-08
"""
import re

from pydantic import BaseModel, EmailStr, field_validator, Field


class UserRegister(BaseModel):
    """
    用户注册类
    @author: Luzhichao
    @date: 2026-05-08
    """
    user_name: str = Field(..., min_length=2, max_length=20, description="用户名(只能包含英文字母和数字)")
    phone: str = Field(..., min_length=11, max_length=11, description="手机号")
    email: EmailStr = Field(..., description="邮箱")
    user_password: str = Field(..., min_length=6, max_length=20, description="密码(只能包含英文字母、数字和常用特殊字符)")

    @field_validator("user_name")
    def validate_username(cls, v):
        if not re.match(r'^[a-zA-Z0-9]+$', v):
            raise ValueError("用户名只能包含英文字母和数字")
        return v

    @field_validator("phone")
    def validate_phone(cls, v):
        if not re.match(r"^1[3-9]\d{9}$", v):
            raise ValueError("手机号格式不正确")
        return v

    @field_validator("user_password")
    def validate_password(cls, v):
        if not re.match(r'^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{}|;:,.<>?]+$', v):
            raise ValueError("密码只能包含英文字母、数字和常用特殊字符")
        return v


class UserLogIn(BaseModel):
    """
    用户登录类
    @author: Luzhichao
    @date: 2026-05-08
    """
    user_name: str = Field(..., min_length=2, max_length=20, description="用户名(只能包含英文字母和数字)")
    user_password: str = Field(..., min_length=6, max_length=20, description="密码(只能包含英文字母、数字和常用特殊字符)")

    @field_validator("user_name")
    def validate_username(cls, v):
        # 只能是英文字母
        if not re.match(r'^[a-zA-Z0-9]+$', v):
            raise ValueError("用户名只能包含英文字母和数字")
        return v

    @field_validator("user_password")
    def validate_password(cls, v):
        if not re.match(r'^[a-zA-Z0-9!@#$%^&*()_+\-=\[\]{}|;:,.<>?]+$', v):
            raise ValueError("密码只能包含英文字母、数字和常用特殊字符")
        return v


class Token(BaseModel):
    """
    登录token对象
    @author: Luzhichao
    @date: 2026-05-08
    """
    user_id: int = None
    user_name: str = None
