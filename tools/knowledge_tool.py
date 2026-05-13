#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026/5/7
"""
import os

from langchain_core.tools import tool
from langchain_tavily import TavilySearch

from core.config import settings
from utils import llm_utils

os.environ['TAVILY_API_KEY'] = settings.tavily_api_key


@tool
def search_knowledge(keywords: list[str]) -> list[str]:
    """
    查找知识库中相关法律法规、判断依据
    :param keywords: 关键词列表
    :return: 返回知识库相关数据
    @author: Luzhichao
    @date: 2026-05-07
    """
    result = []
    for keyword in keywords:
        knowledge = llm_utils.query_knowledge(keyword)
        result.append(knowledge)
    return result


@tool
def web_search(keyword: str) -> list[str]:
    """
    查找相关法律法规、判断依据
    :param keyword 关键词
    :return 法律法规、判断依据
    @author: Luzhichao
    @date: 2026-05-07
    """
    print("=============web_search=============\n", keyword)
    search = TavilySearch(max_results=5, topic="general")
    return search.invoke(keyword)
