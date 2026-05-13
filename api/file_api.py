#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026-05-12
"""
import logging
from typing import Annotated, List

from fastapi import APIRouter, UploadFile, File, Depends, status

from core.config import settings
from core.exceptions import CustomException
from core.response import Result
from core.security import verify_token
from model.file_model import FileResponse
from schema.user_schema import Token

logger = logging.getLogger("file_api")

router = APIRouter(prefix=f"/api/{settings.api_version}/file", tags=["文件管理接口"])

# 允许的风险图片类型
ALLOWED_RISK_IMAGES_MIME_TYPES = {
    "image/jpeg": ".jpeg",
    "image/png": ".png",
    "image/jpg": ".jpg"
}
# 文件大小限制 (5MB)
MAX_FILE_SIZE = 5 * 1024 * 1024

# 测试图片
TEST_RISK_IMAGES = [
    "https://k.sinaimg.cn/n/sinakd20260430s/405/w1080h925/20260430/9d08-8ede80edcd105e1d348a8073c097f9d8.jpg/w700d1q75cms.jpg",
    "https://q7.itc.cn/q_70/images03/20240617/e687d738f97145ad94f4eb13d440c497.jpeg"
]


@router.post(path="/upload_risk_images", summary="风险图片上传",
             description="安全风险图片上传，支持多图片上传(*.jpg、*.png、*.jpeg)，最多5张，每张最大5M")
async def upload_risk_images(
        files: Annotated[List[UploadFile], File(..., description="风险图片")],
        user: Token = Depends(verify_token)):
    """
    安全风险图片上传，支持多图片上传(*.jpg、*.png、*.jpeg)，最多5张，每张最大5M
    :param
    :return
    @author: Luzhichao
    @date: 2026-05-12
    """
    if len(files) > 5:
        raise CustomException(status_code=status.HTTP_400_BAD_REQUEST,
                              detail="最多上传5张图片")
    for file in files:
        # 验证文件类型
        if file.content_type not in ALLOWED_RISK_IMAGES_MIME_TYPES:
            raise CustomException(status_code=status.HTTP_400_BAD_REQUEST,
                                  detail=f"不支持的文件类型。支持: {ALLOWED_RISK_IMAGES_MIME_TYPES}")

        # 读取并验证大小
        content = await file.read()
        file_size = len(content)
        if file_size > MAX_FILE_SIZE:
            raise CustomException(status_code=status.HTTP_400_BAD_REQUEST,
                                  detail=f"文件过大，最大 {MAX_FILE_SIZE // (1024 * 1024)}MB")
        # 重置指针
        await file.seek(0)

        if file_size == 0:
            raise CustomException(status_code=status.HTTP_400_BAD_REQUEST, detail="文件为空")

    return Result.success(data=TEST_RISK_IMAGES, msg="上传成功")


@router.post(path="/upload_knowledge", summary="知识文档上传",
             description="知识上传，支持上传MD、PDF、DOC、DOCX、PPT、PPTX、XLS、XLSX、TXT格式文件，最大10M")
async def upload_knowledge(file: Annotated[UploadFile, File(..., description="知识文档")],
                           user: Token = Depends(verify_token)):
    """
    知识上传，支持上传MD、PDF、DOC、DOCX、PPT、PPTX、XLS、XLSX、TXT格式文件，最大10M
    :param
    :return
    @author: Luzhichao
    @date: 2026-05-12
    """
    result = FileResponse(file_name="test.md", path="", url="", type="md")
    return Result.success(data=result, msg="上传成功")
