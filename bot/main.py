import logging
from urllib.parse import urljoin

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import WebhookInfo
from app.models.database import async_session
from bot.handlers import contact_handler, start_handlers
from bot.middleware import DbMiddleware, UserAuthMiddleware
from config import config

logger = logging.getLogger()
bot = Bot(token=config.BOT_TOKEN.get_secret_value(), default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()

dp.include_routers(start_handlers.router, contact_handler.router)
dp.update.middleware(DbMiddleware(async_session))
dp.update.middleware(UserAuthMiddleware())


async def set_webhook(my_bot: Bot) -> None:
    # Check and set webhook for Telegram
    async def check_webhook() -> WebhookInfo | None:
        try:
            webhook_info = await my_bot.get_webhook_info()
            return webhook_info
        except Exception as e:
            logger.error(f"Can't get webhook info - {e}")
            return

    current_webhook_info = await check_webhook()
    if config.DEBUG:
        logger.debug(f"Current bot info: {current_webhook_info}")
    try:

        webapp_url = urljoin(config.WEBAPP_URL, "webhook")

        await bot.set_webhook(
            webapp_url,
            # secret_token=cfg.telegram_my_token,
            drop_pending_updates=True,
            allowed_updates=dp.resolve_used_update_types(),
        )
        if config.DEBUG:
            logger.debug(f"Updated bot info: {await check_webhook()}")
    except Exception as e:
        logger.error(f"Can't set webhook - {e}")


async def init_bot():
    await set_webhook(bot)
