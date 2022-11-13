import logging
from typing import Dict, Any

from fastapi import FastAPI
from pydantic import BaseModel

from celsiusbot.tgbot import BOT_UPDATE_URL, BOT_UPDATE_ENDPOINT, bot, authorized_user_display, process_update


logging.basicConfig(level=logging.INFO)

app = FastAPI(openapi_url=None)


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
    await process_update(update)
    return {"ok": True}
