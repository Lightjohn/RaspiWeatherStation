# -*- coding: utf-8 -*-
from time import sleep

import bme280

import dataset
from datetime import datetime, timedelta

SLEEP_TIME = 5  # Every X min
db = dataset.connect('sqlite:///weather.db')
table = db['weather']


def sleep_until_exact_time():
    _now = datetime.utcnow()
    clean_now = _now.replace(second=0, microsecond=0)
    _sleep_time = clean_now + timedelta(minutes=SLEEP_TIME - (clean_now.minute % SLEEP_TIME))
    sleep_time_sec = (_sleep_time - _now).total_seconds()
    sleep(sleep_time_sec)


def save_weather():
    temperature, pressure, humidity = bme280.readBME280All()
    # print(f"Temp : {temperature}°C \t P : {pressure}hPa \t HR : {humidity}%")
    _now = datetime.utcnow()
    data = dict(date=_now, temperature=temperature, pressure=pressure, humidity=humidity)
    table.insert(data)
    sleep_until_exact_time()


while True:
    sleep_until_exact_time()
    save_weather()
