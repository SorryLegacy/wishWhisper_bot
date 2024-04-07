import asyncio

from sqlalchemy import select
from httpx import AsyncClient
from fastapi import APIRouter, HTTPException, BackgroundTasks

from config import config
from app.shemas import ResponseFullUser, UpdateUser
from app.models.user_models import User
from app.models.database import db_depend

router = APIRouter(prefix="/api/v1")


async def send_event_to_user(user: User) -> None:
    """
    SEND updated status of user mood
    """
    partner = await user.partner
    loop = asyncio.get_event_loop()
    json = {
        "chat_id": partner.chat_id,
        "text": f"Ваш парнер поменял настроение на {user.mood.value}",
        "parse_mode": "Markdown",
    }
    async with AsyncClient() as client:
        response = await loop.run_in_executor(
            None,
            lambda: client.post(
                f"https://api.telegram.org/bot{config.BOT_TOKEN.get_secret_value()}/sendMessage", json=json
            ),
        )
        await response


@router.get("/user/{user_id}", response_model=ResponseFullUser)
async def get_single_user(user_id: int, db: db_depend):
    user_corutine = await db.execute(select(User).where(User.id == user_id))
    user = user_corutine.scalar()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return ResponseFullUser.model_validate(user)


@router.patch("/user/", response_model=ResponseFullUser)
async def patch_user(update_user: UpdateUser, db: db_depend, background_task: BackgroundTasks):
    user_corutine = await db.execute(select(User).where(User.id == update_user.id))
    user = user_corutine.scalar()
    if user:
        user.mood = update_user.mood
        await db.commit()
        await db.refresh(user)
        background_task.add_task(send_event_to_user, user)
        return ResponseFullUser.model_validate(user)
    else:
        raise HTTPException(status_code=404, detail="User not found")
