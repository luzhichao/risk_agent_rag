# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026/5/7
"""
from snowflake import Snowflake

# 全局单例
snowflake = Snowflake(
    datacenter_id=1,  # 机房ID
    worker_id=1  # 机器ID
)


def next_snowflake_id() -> str:
    """生成雪花ID并返回字符串"""
    return str(snowflake.generate())
