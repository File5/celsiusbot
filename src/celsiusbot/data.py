from datetime import datetime

from celsiusbot.models import SensorData


data = {
    "time": [],
    "temperature": [],
    "humidity": []
}


def append(sensor_data: SensorData):
    now = datetime.now()
    data['time'].append(now)
    data['temperature'].append(sensor_data.temperature)
    data['humidity'].append(sensor_data.humidity)


def is_day_changed():
    last_time = data['time'][-1] if data['time'] else None
    now = datetime.now()
    return last_time is not None and last_time.date() != now.date()


def clear():
    data['time'].clear()
    data['temperature'].clear()
    data['humidity'].clear()


def get_data():
    return data
