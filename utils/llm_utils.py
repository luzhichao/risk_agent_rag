#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026/5/7
"""
import json
import logging
from typing import Optional, AsyncGenerator

from langchain.agents import create_agent
from langchain.agents.middleware import SummarizationMiddleware
from langchain.chat_models import init_chat_model
from langchain_chroma import Chroma
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document
from langchain_core.messages import AIMessageChunk, HumanMessage, BaseMessage, ToolMessage, \
    AIMessage
from langchain_core.runnables import RunnableConfig
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langgraph.checkpoint.redis import RedisSaver
from redis import Redis

from core.config import settings
from model.chat_model import ChatResponse
from model.session_model import SessionHistoryResponse
from tools.knowledge_tool import search_knowledge, web_search

logger = logging.getLogger("llm_utils")

think_nodes = [
    "SummarizationMiddleware.before_model",
    "agent",
    "tools",
    "pre",
    "post"
]

# 多模态模型
multi_llm = init_chat_model(
    model=settings.multimodal_model_name,
    model_provider="openai",
    base_url=settings.base_url,
    api_key=settings.dashscope_api_key
)

# 纯文本模型，形成摘要记忆
text_llm = init_chat_model(
    model=settings.text_model_name,
    model_provider="openai",
    base_url=settings.base_url,
    api_key=settings.dashscope_api_key
)

# 嵌入模型
embeddings_model = DashScopeEmbeddings(
    model=settings.embedding_model_name,
)

# 创建向量数据库
chromadb = Chroma(
    embedding_function=embeddings_model,
    persist_directory=settings.chroma_persist_directory,
    collection_name=settings.chroma_collection_name
)

redis_client = Redis(
    host=settings.redis_host,
    port=settings.redis_port,
    password=settings.redis_password,
    decode_responses=False
)

# Pass the configured client to RedisSaver
redis_checkpointer = RedisSaver(redis_client=redis_client)
middleware = SummarizationMiddleware(model=text_llm, trigger=("tokens", 100), keep=("messages", 5))

with open(settings.system_prompt_file_path, "r", encoding="utf-8") as f:
    system_prompt = f.read()

agent = create_agent(model=multi_llm,
                     system_prompt=system_prompt,
                     tools=[search_knowledge, web_search],
                     middleware=[middleware],
                     checkpointer=redis_checkpointer,
                     response_format=ChatResponse,
                     )


async def chat(
        text: str,
        session_id: str,
        images: Optional[list[str]] = None,
) -> AsyncGenerator[str, None]:
    """
    会话接口
    @author: Luzhichao
    @date: 2026-05-07
    """
    # 构建消息
    messages = [{"type": "text", "text": text}]
    if images and len(images) > 0:
        for image in images:
            messages.append({"type": "image", "url": image})
    # 配置会话ID
    config: RunnableConfig = {"configurable": {"thread_id": session_id}}
    try:
        stream = agent.stream(input={"messages": [HumanMessage(content=messages)]}, config=config,
                              stream_mode="messages")
        for chunk, metadata in stream:
            # print("-" * 50, type(chunk))
            # print(metadata)
            source = metadata.get("langgraph_node", "")
            if isinstance(chunk, AIMessageChunk) and chunk.content:
                if source == "model":
                    data = {"type": "output", "content": chunk.content}
                else:
                    data = {"type": "think", "content": chunk.content}
                # print("=" * 50)
                # print(data, end="", flush=True)
                yield json.dumps(data, ensure_ascii=False)
    except Exception as e:
        logger.error(f"会话接口异常：{str(e)}")
        error_content = {"type": "output", "content": f"会话接口异常：{str(e)}"}
        yield json.dumps(error_content, ensure_ascii=False)


def get_history(session_id: str):
    """
    获取历史会话接口
    @author: Luzhichao
    @date: 2026-05-07
    """
    # 配置会话ID
    config: RunnableConfig = {"configurable": {"thread_id": session_id}}
    history = redis_checkpointer.get(config=config)
    session_history: list[SessionHistoryResponse] = []
    if history is not None:
        channel_values = history.get("channel_values", None)
        if channel_values is not None:
            messages: list[BaseMessage] = channel_values.get("messages", [])
            if len(messages) > 0:
                for message in messages:
                    if isinstance(message, HumanMessage) | isinstance(message, AIMessage):
                        if is_valid_content(message.content):
                            session_history.append(
                                SessionHistoryResponse(type=message.type, content=message.content))
                    elif isinstance(message, ToolMessage):
                        message.pretty_print()
                        continue

    return session_history


def clean_history(session_id: str):
    """
    清空历史会话接口
    @author: Luzhichao
    @date: 2026-05-07
    """
    redis_checkpointer.delete_thread(thread_id=session_id)


def save_knowledge(docs: list[Document]):
    """
    知识库保存接口
    @author: Luzhichao
    @date: 2026-05-07
    """
    # 创建文本分块器
    splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=20,
                                              separator=["。", ";"])
    # 分块
    documents = splitter.split_documents(documents=docs)
    # 向量数据存储
    chromadb.add_documents(documents=documents)


def query_knowledge(query: str, search_type: str = "mmr", k: int = 3) -> list[str]:
    """
    知识库查询接口
    @author: Luzhichao
    @date: 2026-05-07
    """
    docs = chromadb.search(query=query, search_type=search_type, k=k)
    result = []
    for doc in docs:
        if doc.page_content:
            result.append(doc.page_content)

    return result


def is_valid_content(content: str | list[str | dict] | None) -> bool:
    """
    判断 content 是否有效：
    - 不为 None
    - 不为空字符串 ""
    - 不为空列表 []
    :param
    :return
    @author: Luzhichao
    @date: 2026-05-09
    """
    if content is None:
        return False

    if isinstance(content, str):
        return len(content.strip()) > 0

    if isinstance(content, list):
        return len(content) > 0

    return False
