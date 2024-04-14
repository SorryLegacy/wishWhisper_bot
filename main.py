from contextlib import asynccontextmanager
from typing import AsyncGenerator

from aiogram.types import Update
from app.route import router
from bot.main import bot, dp, init_bot
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates


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


@app.exception_handler(404)
async def custom_404_handler(request, __):
    return templates.TemplateResponse(request=request, name="404.html")


@app.get("/webapp/mood", response_class=HTMLResponse)
async def mood_html_render(request: Request):
    return templates.TemplateResponse(request=request, name="main.html")


@app.get("/webapp/wish", response_class=HTMLResponse)
async def add_wish_render(requset: Request):
    return templates.TemplateResponse(request=requset, name="add-wish.html")


@app.get("/webapp/my-wish", response_class=HTMLResponse)
async def my_wish_list(requset: Request):
    return templates.TemplateResponse(request=requset, name="list-wish.html")


@app.get("/webapp/partner-wish", response_class=HTMLResponse)
async def partner_wish_list(requset: Request):
    return templates.TemplateResponse(request=requset, name="list-wish.html")
