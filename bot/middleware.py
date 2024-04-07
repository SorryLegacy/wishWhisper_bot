from typing import Any, Awaitable, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from app.models import User
from sqlalchemy import exists, select
from sqlalchemy.ext.asyncio import async_sessionmaker


class DbMiddleware(BaseMiddleware):

    def __init__(self, session_pool: async_sessionmaker):
        super().__init__()
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:

        async with self.session_pool() as session:
            data["session"] = session
            return await handler(event, data)


class UserAuthMiddleware(BaseMiddleware):

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:

        user_id = data["event_from_user"].id
        query = select(exists().where(User.id == user_id))
        session = data.get("session")
        user_exists_corutine = await session.execute(query)
        user_exists = user_exists_corutine.scalar()
        if not user_exists:
            chat_id = data["event_chat"].id

            user = User(id=user_id, chat_id=chat_id)
            session.add(user)
            await session.commit()
        else:
            user_corutine = await session.execute(select(User).where(User.id == user_id))
            user = user_corutine.scalar()
        data["chat_user"] = user
        return await handler(event, data)
