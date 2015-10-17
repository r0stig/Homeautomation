from datetime import datetime, date
from astral import *
from pytz import timezone


gothenburg_latitude = 57.7136505
gothenburg_longitude =  11.9957975


def get_today_sunset():
    a = Astral()

    sunset_datetime = a.sunset_utc(date.today(), gothenburg_latitude, gothenburg_longitude)
    sunrise_datetime = a.sunrise_utc(date.today(), gothenburg_latitude, gothenburg_longitude)

    sunrise_datetime = sunrise_datetime.astimezone(timezone('Europe/Stockholm'))
    sunset_datetime = sunset_datetime.astimezone(timezone('Europe/Stockholm'))

    return sunset_datetime

def get_today_sunrise():
    a = Astral()

    sunset_datetime = a.sunset_utc(date.today(), gothenburg_latitude, gothenburg_longitude)
    sunrise_datetime = a.sunrise_utc(date.today(), gothenburg_latitude, gothenburg_longitude)

    sunrise_datetime = sunrise_datetime.astimezone(timezone('Europe/Stockholm'))
    sunset_datetime = sunset_datetime.astimezone(timezone('Europe/Stockholm'))

    return sunrise_datetime

