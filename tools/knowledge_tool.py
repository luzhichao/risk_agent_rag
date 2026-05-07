#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026/5/7
"""

from langchain_core.tools import tool

from utils import llm_utils


@tool
def search_knowledge(keywords: list[str]) -> list[str]:
    """
    知识库搜索
    :param keywords: 关键字列表
    :return: 返回知识库相关数据
    @author: Luzhichao
    @date: 2026-05-07
    """
    result = []
    for keyword in keywords:
        knowledge = llm_utils.query_knowledge(keyword)
        result.append(knowledge)
    return result
