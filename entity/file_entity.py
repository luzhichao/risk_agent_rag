# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026-5-12
"""
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from entity.base_entity import BaseEntity


class FileEntity(BaseEntity):
    """
    文件数据实体
    @author: Luzhichao
    @date: 2026-05-12
    """
    __tablename__ = "t_file"

    file_name: Mapped[str] = mapped_column("file_name", String(255), nullable=False,
                                           comment="文件名称")
    type: Mapped[str] = mapped_column("file_type", String(255), nullable=False,
                                      comment="文件类型")
    path: Mapped[str] = mapped_column("file_path", String(255), nullable=False,
                                      comment="文件路径")
    url: Mapped[str] = mapped_column("file_url", String(255), nullable=False,
                                     comment="可访问URL")
    size: Mapped[int] = mapped_column("file_size", String(100), nullable=False,
                                      comment="文件大小")
