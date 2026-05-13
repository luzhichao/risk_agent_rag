# !/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026-05-12
"""
import logging

from fastapi import APIRouter, Depends, Body

from core.config import settings
from core.response import Result
from core.security import verify_token
from model.knowledge_model import KnowledgeResponse
from schema.knowledge_schema import Knowledge
from schema.user_schema import Token

logger = logging.getLogger("knowledge_api")

router = APIRouter(prefix=f"/api/{settings.api_version}/knowledge", tags=["知识库管理接口"])


@router.post(path="/creat", summary="新增知识库信息", description="根据上传的文件创建知识库信息")
def creat_knowledge_info(
        knowledge: Knowledge = Body(..., description="文档信息"),
        user: Token = Depends(verify_token)
):
    """
    新增知识库信息
    :param
    :return
    @author: Luzhichao
    @date: 2026-05-12
    """
    return Result.success(msg="保存成功")


@router.post(path="/update", summary="更新知识库信息",
             description="根据上传的文件更新知识库信息，已完成知识库分块存储不能更新文件只能更新名称")
def update_knowledge_info(
        doc_id: str = Body(..., description="文档ID"),
        knowledge: Knowledge = Body(..., description="文档信息"),
        user: Token = Depends(verify_token)
):
    """
    更新知识库信息
    :param
    :return
    @author: Luzhichao
    @date: 2026-05-12
    """
    return Result.success(msg="更新成功")


@router.post(path="/delete", summary="删除知识库信息",
               description="删除知识库信息，已完成知识库分块存储不能删除")
def delete_knowledge_document(
        doc_id: str = Body(..., description="文档ID"),
        user: Token = Depends(verify_token)
):
    """
    删除知识库信息
    :param
    :return
    @author: Luzhichao
    @date: 2026-05-12
    """
    return Result.success(msg="删除成功")


@router.post(path="/list", summary="查询知识库信息", description="查询知识库信息")
def list_knowledge_documents(
        user: Token = Depends(verify_token)
):
    """
    查询知识库信息
    :param
    :return
    @author: Luzhichao
    @date: 2026-05-12
    """
    result = KnowledgeResponse(doc_id="", knowledge_name="", type="", status="", path="", url="")
    return Result.success(data=[result], msg="查询成功")


@router.post(path="/embedding", summary="指定ID知识库分块存储", description="指定ID知识库分块存储")
def get_knowledge_chunks(
        doc_id: str = Body(..., description="文档ID"),
        user: Token = Depends(verify_token)
):
    """
    指定ID知识库分块存储
    :param
    :return
    @author: Luzhichao
    @date: 2026-05-12
    """
    return Result.success(msg="知识库构建成功")
