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


def add_time(time: timedelta):
    """
    北京当前时间增加时间
    :param
    :return
    @author: Luzhichao
    @date: 2026-05-08
    """
    return now_time() + time
