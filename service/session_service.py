#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
@author: luzhichao
@date: 2026-05-09
"""
import logging

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.exceptions import CustomException
from entity import SessionEntity
from model.session_model import SessionResponse
from utils import llm_utils

logger = logging.getLogger("session_service")


class SessionService:
    """
    会话服务
    @author: Luzhichao
    @date: 2026-05-09
    """

    @staticmethod
    async def create_new_session(db: AsyncSession, user_id: str, session_name: str) -> str:
        """
        创建新会话
        :param db 数据库连接
        :param user_id: 用户ID
        :param session_name: 会话名称
        :return:
        @author: Luzhichao
        @date: 2026-05-09
        """
        session_entity = SessionEntity(user_id=user_id, session_name=session_name)
        try:
            db.add(session_entity)
            await db.commit()
            await db.refresh(session_entity)
            return session_entity.id
        except Exception as e:
            logger.error(e)
            await db.rollback()
            raise CustomException(detail="创建会话失败")

    @staticmethod
    async def get_user_sessions(db: AsyncSession, user_id: str, session_id: str):
        """
        获取用户会话
        :param db: 数据库连接
        :param user_id: 用户ID
        :param session_id 会话ID
        :return:
        @author: Luzhichao
        @date: 2026-05-09
        """
        try:
            execute = await db.execute(
                select(SessionEntity)
                .filter(SessionEntity.user_id == user_id)
                .filter(SessionEntity.id == session_id)
            )
            session: SessionEntity = execute.scalar_one_or_none()
            if session is not None:
                return SessionResponse(session_id=session.id, session_name=session.session_name,
                                       user_id=session.user_id)
            else:
                return None

        except Exception as e:
            logger.error(e)
            raise CustomException(detail="获取会话失败")

    @staticmethod
    async def list_user_sessions(db: AsyncSession, user_id: str):
        """
        获取用户会话列表
        :param db: 数据库连接
        :param user_id: 用户ID
        :return:
        @author: Luzhichao
        @date: 2026-05-09
        """
        try:
            execute = await db.execute(
                select(SessionEntity).filter(SessionEntity.user_id == user_id))
            session_list = execute.scalars().all()
            result = []
            for session in session_list:
                result.append(
                    SessionResponse(session_id=session.id, session_name=session.session_name,
                                    user_id=session.user_id))

            return result
        except Exception as e:
            logger.error(e)
            raise CustomException(detail="获取会话列表失败")

    @staticmethod
    async def session_history(session_id: str, user_id: str, db: AsyncSession):
        """
        获取会话历史
        :param
        :return
        @author: Luzhichao
        @date: 2026-05-09
        """
        execute = await db.execute(
            select(SessionEntity)
            .filter(SessionEntity.user_id == user_id)
            .filter(SessionEntity.id == session_id)
        )
        session: SessionEntity = execute.scalar_one_or_none()
        if session is not None:
            return llm_utils.get_history(session.id)
        else:
            raise CustomException(detail="会话不存在")

    @staticmethod
    async def clear_session_history(
            session_id: str,
            user_id: str,
            db: AsyncSession):
        """
        会话历史清空
        :param
        :return
        @author: Luzhichao
        @date: 2026-05-09
        """
        execute = await db.execute(
            select(SessionEntity)
            .filter(SessionEntity.user_id == user_id)
            .filter(SessionEntity.id == session_id)
        )
        session: SessionEntity = execute.scalar_one_or_none()
        if session is not None:
            try:
                llm_utils.clean_history(session_id)
                await db.delete(session)
                await db.commit()
            except Exception as e:
                logger.error(f"清空会话失败:{e}")
                raise CustomException(detail="清空会话失败")
        else:
            raise CustomException(detail="会话不存在")
