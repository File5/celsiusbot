import logging
from typing import Dict, Any

from fastapi import FastAPI

from celsiusbot.tgbot import BOT_UPDATE_URL, BOT_UPDATE_ENDPOINT, bot, authorized_user_display, \
    process_update, update_display
from celsiusbot.socket import sio, create_app, SensorData


logging.basicConfig(level=logging.INFO)

app = FastAPI(openapi_url=None)


@app.on_event("startup")
async def startup_event():
    await bot.set_webhook(BOT_UPDATE_URL)

@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/sensor")
async def sensor(sensor_data: SensorData):
    if authorized_user_display.get("chat_id") is not None:
        await update_display(sensor_data)
    return {"message": "OK"}

@app.post(BOT_UPDATE_ENDPOINT)
async def bot_update(update: Dict[str, Any]):
    await process_update(update)
    return {"ok": True}

app = create_app(sio, app)
