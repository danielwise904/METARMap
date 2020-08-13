import datetime
import astral
from astral import LocationInfo
from astral.geocoder import database, lookup
from astral.sun import sun

CITY = "Austin"
LED_DAY_BRIGHTNESS	= 0.2				# Float from 0.0 (min) to 1.0 (max)
LED_NIGHT_BRIGHTNESS= 0.08				# Float from 0.0 (min) to 1.0 (max)

now_utc = datetime.datetime.utcnow()
now_local = datetime.datetime.now()
year = now_local.date().year
month = now_local.date().month
day = now_local.date().day
city = lookup(CITY,database())
s = sun(city.observer, date=datetime.date(year, month, day))
sunrise = (s["sunrise"]).replace(tzinfo=None)
sunset = (s["sunset"]).replace(tzinfo=None)
dawn = (s["dawn"]).replace(tzinfo=None)
dusk = (s["dusk"]).replace(tzinfo=None)
up = sunrise
down = sunset
if ((now_utc < up) | (now_utc > down)):
	LED_BRIGHTNESS = LED_NIGHT_BRIGHTNESS
	print("Nightime. Switching at " + str(up))
elif ((now_utc > up) & (now_utc < down)):
	LED_BRIGHTNESS = LED_DAY_BRIGHTNESS
	print("Daytime. Switching at " + str(down))
else:
	LED_BRIGHTNESS = LED_DAY_BRIGHTNESS
	print("Time error. Setting brightness to day.")