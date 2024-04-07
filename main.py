from typing import AsyncGenerator
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


from bot.main import init_bot, bot, dp
from app.route import router
from aiogram.types import Update


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator:
    await init_bot()
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="app/static"), name="static")
app.include_router(router)
templates = Jinja2Templates(directory="app/templates")


@app.post("/webhook")
async def webhook(update: dict) -> None:
    """
    Webhook for tg bot
    Not polling
    """
    tg_updates = Update(**update)
    await dp.feed_webhook_update(bot=bot, update=tg_updates)


@app.get("/webapp", response_class=HTMLResponse)
async def html_test(request: Request):
    return templates.TemplateResponse(request=request, name="main.html")
