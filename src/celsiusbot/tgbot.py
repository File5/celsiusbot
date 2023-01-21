from typing import Dict, Any

from aiogram import Bot, Dispatcher, types

from celsiusbot.data import append, get_data, clear, is_day_changed
from celsiusbot.plot import generate_plot
from celsiusbot.models import SensorData
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

async def update_display(sensor_data: SensorData):
    day_changed = is_day_changed()
    print(f"is_day_changed() = {day_changed}")
    if day_changed:
        generate_plot(get_data())
        clear()
        await bot.delete_message(
            chat_id=authorized_user_display["chat_id"],
            message_id=authorized_user_display["message_id"],
        )
        authorized_user_display["message_id"] = None
        with open("plot.png", "rb") as plot_file:
            await bot.send_photo(
                chat_id=authorized_user_display["chat_id"],
                photo=plot_file,
            )

    append(sensor_data)
    
    text = "🏠Home\n🌡️ {:.1f} °C 💧 {:.0f} %".format(sensor_data.temperature, sensor_data.humidity)
    if authorized_user_display["message_id"] is None:
        message = await bot.send_message(
            chat_id=authorized_user_display["chat_id"],
            text=text,
        )
        authorized_user_display["message_id"] = message.message_id
    else:
        await bot.edit_message_text(
            text=text,
            chat_id=authorized_user_display["chat_id"],
            message_id=authorized_user_display["message_id"],
        )
