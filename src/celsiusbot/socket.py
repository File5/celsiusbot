import json
from typing import Dict, Any

import socketio

from celsiusbot.models import SensorData
from celsiusbot.tgbot import update_display

sio = socketio.AsyncServer(async_mode="asgi", cors_allowed_origins="*")


@sio.event
async def data(sid: str, data: Dict[str, Any]):
    sensor_data = SensorData(**data)
    await update_display(sensor_data)

def create_app(sio, other_app):
    return socketio.ASGIApp(sio, other_app)
