# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026-5-12
"""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from entity.base_entity import BaseEntity


class KnowledgeEntity(BaseEntity):
    """
    知识库文档数据实体
    @author: Luzhichao
    @date: 2026-05-12
    """
    __tablename__ = "t_knowledge"

    knowledge_name: Mapped[str] = mapped_column("knowledge_name", String(255), nullable=False,
                                                comment="知识名称")
    type: Mapped[str] = mapped_column("type", String(255), nullable=False, comment="知识类型")
    status: Mapped[str] = mapped_column("status", String(255), nullable=False,
                                        default="unfinished",
                                        comment="知识状态，是否完成知识库构建")
    path: Mapped[str] = mapped_column("path", String(255), nullable=False, comment="知识路径")
    url: Mapped[str] = mapped_column("url", String(255), nullable=False,
                                     comment="知识文档可访问的URL")
