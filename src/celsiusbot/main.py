import asyncio
import logging
from typing import Dict, Any

from fastapi import FastAPI
from aiogram import Bot, Dispatcher, types
from pydantic import BaseModel

from celsiusbot.settings import BOT_TOKEN, HOST, AUTHORIZED_USER_ID

logging.basicConfig(level=logging.INFO)

app = FastAPI(openapi_url=None)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

BOT_UPDATE_ENDPOINT = f"/bot{BOT_TOKEN}/"
BOT_UPDATE_URL = f"https://{HOST}{BOT_UPDATE_ENDPOINT}"

authorized_user_display = {
    "chat_id": None,
    "message_id": None,
}


class SensorData(BaseModel):
    temperature: float
    humidity: float


@app.on_event("startup")
async def startup_event():
    await bot.set_webhook(BOT_UPDATE_URL)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/sensor")
async def sensor(sensor_data: SensorData):
    if authorized_user_display.get("chat_id") is not None:
        text = "🏠Home\n🌡️ {:.1f} °C 💧 {:.0f} %".format(sensor_data.temperature, sensor_data.humidity)
        await bot.edit_message_text(
            text=text,
            chat_id=authorized_user_display["chat_id"],
            message_id=authorized_user_display["message_id"]
        )
    return {"message": "OK"}

@app.post(BOT_UPDATE_ENDPOINT)
async def bot_update(update: Dict[str, Any]):
    update = types.Update(**update)
    Bot.set_current(bot)
    Dispatcher.set_current(dp)
    await dp.process_update(update)
    return {"ok": True}

@dp.message_handler()
async def echo(message: types.Message):
    answer = await message.answer(message.text)
    if message.from_user.id == AUTHORIZED_USER_ID:
        authorized_user_display["chat_id"] = answer.chat.id
        authorized_user_display["message_id"] = answer.message_id
