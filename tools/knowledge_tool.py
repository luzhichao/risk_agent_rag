#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026/5/7
"""
from langchain_core.tools import tool


@tool
def search_knowledge(keyword: str) -> list[str]:
    """
    知识库搜索
    :param keyword: 关键字
    :return: 返回知识库相关数据
    @author: Luzhichao
    @date: 2026-05-07
    """
    pass
