#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026/5/7
"""
from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain.chat_models import init_chat_model
from langchain_community.chat_models.tongyi import ChatTongyi
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.messages import AIMessageChunk, HumanMessage
from langgraph.checkpoint.redis import RedisSaver
from redis import Redis

from core.config import settings
from model.chat_model import ChatResponse
from tools.knowledge_tool import search_knowledge

# 多模态模型
multi_llm = init_chat_model(
    model=settings.multimodal_model_name,
    model_provider="openai",
    base_url=settings.base_url,
    api_key=settings.dashscope_api_key
)

# 纯文本模型，形成摘要记忆
text_llm = ChatTongyi(
    model=settings.text_model_name,
    api_key=settings.dashscope_api_key,
)

# 嵌入模型
embeddings_model = DashScopeEmbeddings(
    model="text-embedding-v4",
)

redis_client = Redis(
    host="127.0.0.1",
    port=6379,
    password="",
    decode_responses=False
)

# Pass the configured client to RedisSaver
redis_checkpointer = RedisSaver(redis_client=redis_client)

middleware = SummarizationMiddleware(model=text_llm, trigger=("tokens", 100), keep=("messages", 5))

with open(settings.system_prompt_file_path, "rb") as f:
    system_prompt = f.read()

agent = create_agent(model=multi_llm,
                     system_prompt=system_prompt,
                     tools=[search_knowledge],
                     middleware=[middleware],
                     checkpointer=redis_checkpointer,
                     response_format=ChatResponse,
                     )


async def chat(
        text: str,
        session_id: str,
        images: list[str] = None,
):
    """
    会话接口
    @author: Luzhichao
    @date: 2026-05-07
    """
    # 构建消息
    messages = [{"type": "text", "text": f"${text}"}]
    if images and len(images) > 0:
        for image in images:
            messages.append({"type": "image", "url": f"${image}"})
    # 配置会话ID
    config = {"configurable": {"thread_id": f"${session_id}"}}
    try:
        stream = agent.stream(input={"messages": [HumanMessage(content=messages)]}, config=config,
                              stream_mode="messages")
        for chunk, metadata in stream:
            # print("-" * 50, type(chunk))
            # print(chunk)
            if isinstance(chunk, AIMessageChunk) and chunk.content:
                # print(chunk.content, end="", flush=True)
                yield chunk.content
    except Exception as e:
        raise Exception(f"会话接口异常：{str(e)}")


def get_history(session_id: str):
    """
    获取历史会话接口
    @author: Luzhichao
    @date: 2026-05-07
    """
    # 配置会话ID
    config = {"configurable": {"thread_id": f"${session_id}"}}
    return redis_checkpointer.get(config=config)["channel_values"]["messages"]


def clean_history(session_id: str):
    """
    清空历史会话接口
    @author: Luzhichao
    @date: 2026-05-07
    """
    redis_checkpointer.delete_thread(session_id)
