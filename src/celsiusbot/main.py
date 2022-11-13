import asyncio
import logging
from typing import Dict, Any

from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types

from celsiusbot.settings import BOT_TOKEN, HOST

logging.basicConfig(level=logging.INFO)

app = FastAPI(openapi_url=None)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

BOT_UPDATE_ENDPOINT = f"/bot{BOT_TOKEN}/"
BOT_UPDATE_URL = f"https://{HOST}{BOT_UPDATE_ENDPOINT}"

@app.on_event("startup")
async def startup_event():
    await bot.set_webhook(BOT_UPDATE_URL)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post(BOT_UPDATE_ENDPOINT)
async def bot_update(update: Dict[str, Any]):
    update = types.Update(**update)
    Bot.set_current(bot)
    Dispatcher.set_current(dp)
    await dp.process_update(update)
    return {"ok": True}

@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)
