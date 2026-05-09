#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026-05-08
"""
from datetime import datetime, timezone, timedelta


def now_time() -> datetime:
    """
    获取北京当前时间
    :param
    :return
    @author: Luzhichao
    @date: 2026-05-08
    """
    beijing_time = datetime.now(timezone(timedelta(hours=8)))
    return beijing_time


def now_timestamp() -> int:
    """
    获取北京当前时间时间戳(毫秒)
    :param
    :return
    @author: Luzhichao
    @date: 2026-05-08
    """
    beijing_time = datetime.now(timezone(timedelta(hours=8)))
    return int(beijing_time.timestamp() * 1000)


def add_time(time: timedelta):
    """
    北京当前时间增加时间
    :param
    :return
    @author: Luzhichao
    @date: 2026-05-08
    """
    return now_time() + time
