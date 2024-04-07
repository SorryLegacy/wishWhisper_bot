from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from app.models import User, UserPair
from bot.keyboards.buttons import approve_pair, pair_keyboard

router = Router()


@router.message(Command("start"))
async def start_handler(msg: Message, chat_user: User) -> None:
    user_info = msg.from_user
    user_pair: UserPair = await chat_user.pair
    if not user_pair:
        await msg.answer(f"Hi {user_info.first_name}")
    elif not user_pair.is_approved and user_pair.main_user_id != chat_user.id:
        await msg.answer("Test", reply_markup=approve_pair.as_markup())
    elif user_pair.is_approved:
        await msg.answer("У вас есть пара!")
    else:
        await msg.answer("Ждите ответа от партнера")


@router.message(Command("mood"))
async def mood_webapp(msg: Message, chat_user: User) -> None:
    await msg.answer(text="Поменять настроение", reply_markup=pair_keyboard.as_markup())
