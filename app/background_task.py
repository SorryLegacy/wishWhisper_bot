from app.models import User
from bot.main import bot


async def send_event_to_user_partner(user: User, msg: str) -> None:
    """
    SEND message to user partne about chcagne some statuses
    """
    partner: User = await user.partner
    await bot.send_message(chat_id=partner.chat_id, text=msg)
