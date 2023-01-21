from datetime import datetime

from celsiusbot.models import SensorData


data = {
    "time": [],
    "temperature": [],
    "humidity": []
}


def append(data: SensorData) -> bool:
    day_changed = False
    last_time = data['time'][-1] if data['time'] else None
    now = datetime.now()
    if last_time is not None and last_time.date() != now.date():
        day_changed = True
        clear()
    data.time.append(now)
    data.temperature.append(data.temperature)
    data.humidity.append(data.humidity)
    return day_changed


def clear():
    data.time.clear()
    data.temperature.clear()
    data.humidity.clear()


def get_data():
    return data
