from aiogram.utils.markdown import hlink
from app.background_task import send_event_to_user_partner
from app.models.database import db_depend
from app.models.user_models import User
from app.models.wish_models import Wish
from app.shemas import CreateWish, ResponseFullUser, UpdateUser
from fastapi import APIRouter, BackgroundTasks, HTTPException, Response
from sqlalchemy import func, select

router = APIRouter(prefix="/api/v1")


@router.get("/user/{user_id}", response_model=ResponseFullUser)
async def get_single_user(user_id: int, db: db_depend):
    user = await db.scalar(select(User).where(User.id == user_id))
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    else:
        return ResponseFullUser.model_validate(user)


@router.patch("/user/", response_model=ResponseFullUser)
async def patch_user(update_user: UpdateUser, db: db_depend, background_task: BackgroundTasks):
    user = await db.scalar(select(User).where(User.id == update_user.id))

    if user:
        user.mood = update_user.mood
        await db.commit()
        await db.refresh(user)
        background_task.add_task(
            send_event_to_user_partner, user, f"Ваш парнер поменял настроение на {user.mood.value}"
        )
        return ResponseFullUser.model_validate(user)
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.post("/wish")
async def create_wish(wish: CreateWish, db: db_depend, background_task: BackgroundTasks) -> int:
    user = await db.scalar(select(User).where(User.id == wish.user_id))
    if user:
        wish = Wish(**wish.model_dump())
        db.add(wish)
        await db.commit()
        if wish.url:
            link = hlink(wish.name, wish.url)
        else:
            link = wish.name
        count_wish = await db.scalar(select(func.count("*").label("total")).where(Wish.user_id == user.id))
        background_task.add_task(
            send_event_to_user_partner,
            user,
            f"Ваш партнер добавил добавил новой товар {link}.\
    На данный момент длина списка равна {count_wish}",
        )
        return Response()
    else:
        raise HTTPException(status_code=404, detail="User not found")


@router.get("/{user_id}/wish")
async def show_your_wish(user_id: int, db: db_depend):  # TODO need to refactor
    wishes = await db.scalars(select(Wish).where(Wish.user_id == user_id))
    return [wish for wish in wishes]


@router.get("/{user_id}/partner/wish")
async def show_parner_wish(user_id: int, db: db_depend):
    user = await db.scalar(select(User).where(User.id == user_id))  # TODO need to refactor
    partner = await user.partner
    wishes = await db.scalars(select(Wish).where(Wish.user_id == partner.id).order_by(-Wish.prioritet))
    return [wish for wish in wishes]
