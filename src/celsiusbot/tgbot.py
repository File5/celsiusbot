from typing import Dict, Any

from aiogram import Bot, Dispatcher, types

from celsiusbot.settings import BOT_TOKEN, HOST, AUTHORIZED_USER_ID

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

BOT_UPDATE_ENDPOINT = f"/bot{BOT_TOKEN}/"
BOT_UPDATE_URL = f"https://{HOST}{BOT_UPDATE_ENDPOINT}"

authorized_user_display = {
    "chat_id": None,
    "message_id": None,
}

@dp.message_handler()
async def echo(message: types.Message):
    answer = await message.answer(message.text)
    if message.from_user.id == AUTHORIZED_USER_ID:
        authorized_user_display["chat_id"] = answer.chat.id
        authorized_user_display["message_id"] = answer.message_id

async def process_update(update: Dict[str, Any]):
    update = types.Update(**update)
    Bot.set_current(bot)
    Dispatcher.set_current(dp)
    await dp.process_update(update)
