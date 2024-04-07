from aiogram import F, Router, Bot
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import User, UserPair

router = Router()


@router.message(F.contact)
async def create_user(msg: Message, chat_user: User, session: AsyncSession, bot: Bot) -> None:
    user_id = msg.contact.user_id
    user_corutine = await session.execute(select(User).where(User.id == user_id))
    user = user_corutine.scalar()
    if not user:
        user = User(id=user_id, chat_id=user_id)
        session.add(user)

    pair = await chat_user.pair
    pair_2 = await user.pair
    if not any((pair, pair_2)):
        pair = UserPair(main_user_id=chat_user.id, second_user_id=user_id)
        session.add(pair)

        await session.commit()
        await bot.send_message(user_id, "Вам предлагают")

    elif pair.id == pair_2.id:
        await msg.answer("Это ваш партнер")

    elif pair:
        await msg.answer("У вас уже есть пара!")
    elif pair_2:
        await msg.answer("У этого человека уже есть пара")


@router.callback_query(lambda c: c.data == "approve_pair")
async def approve_pair(callback_query: CallbackQuery, chat_user: User, session: AsyncSession) -> None:
    print("here")
    pair: UserPair = await chat_user.pair
    pair.is_approved = True
    session.add(pair)  # TODO fix ?
    await session.commit()
    await callback_query.answer("Ваша пара подтверждена")


@router.callback_query(lambda c: c.data == "delete_pair")
async def delete_pair(callback_query: CallbackQuery, chat_user: User, session: AsyncSession, bot: Bot) -> None:
    pair: UserPair = await chat_user.pair
    user: User = pair.main_user_id if chat_user.id != pair.main_user_id else pair.second_user_id
    await bot.send_message(user.chat_id, text="Ваша пара отказалсь от вас!")
    await session.delete(pair)
    await callback_query.answer("Пара Удаленна")


@router.message(F.text)
async def liza_lubimka(msg: Message, bot: Bot) -> None:
    if msg.from_user.id != 6927423907 and msg.from_user.id == 470184649:  # 6927423907
        text = msg.text + ", Любимка"
        await bot.send_message(chat_id=6927423907, text=text)  # 6927423907
    elif msg.from_user.id == 6927423907:
        text = msg.text
        await bot.send_message(chat_id=470184649, text=text)  #
