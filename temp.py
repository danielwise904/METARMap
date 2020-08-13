#!/usr/bin/env python3

import urllib.request
import xml.etree.ElementTree as ET
import board
import neopixel
import time
import numpy

# NeoPixel LED Configuration
LED_COUNT			= 150				# Number of LED pixels.
LED_PIN				= board.D18			# GPIO pin connected to the pixels (18 is PCM).
LED_BRIGHTNESS		= 0.2				# Float from 0.0 (min) to 1.0 (max)
LED_ORDER			= neopixel.GRB		# Strip type and colour ordering

# COLOR_NEG		= (38,157,176)		# Magenta
# COLOR_0			= (57,102,183)		# Violet
# COLOR_10		= (82,62,181)		# Undigo
# COLOR_20		= (120,86,251)		# Ultramarine
# COLOR_30		= (168,4,244)		# Bright Blue
# COLOR_40		= (188,3,211)		# Turquoise Blue
# COLOR_50		= (149,0,136)		# Emerald Green
# COLOR_60		= (154,40,37)		# Green
# COLOR_70		= (193,138,73)		# Yellow Green
# COLOR_80		= (194,254,8)		# Yellow
# COLOR_90		= (151,255,5)		# Golden Yellow
# COLOR_100		= (87,253,33)		# Orange
# COLOR_RED		= (0,255,0)			# Red
# COLOR_CLEAR 	= (0,0,0)			# Clear

COLOR_NEG		= (0,255,255)		# Pink
COLOR_0			= (0,204,255)		# Magenta
COLOR_10		= (0,153,255)		# Purple
COLOR_20		= (0,102,255)		# Indigo
COLOR_30		= (0,0,255)			# Blue
COLOR_40		= (102,0,255)		# Light Periwinkle
COLOR_50		= (255,0,255)		# Turquoise
COLOR_60		= (255,0,0)			# Green
COLOR_70		= (255,255,0)		# Yellow
COLOR_80		= (153,255,0)		# Light Orange
COLOR_90		= (51,255,0)		# Dark Orange
COLOR_100		= (0,255,0)			# Red 
COLOR_HOT		= (255,255,255)		# White
COLOR_CLEAR 	= (0,0,0)			# Clear

# Wet Bulb Threshold
WET_BULB_THRESHOLD = 27.8			# Float in degrees C

# Heat Index Threshold
HEAT_INDEX_THRESHOLD = 100			# Float in degrees F

# Blinking Speed in seconds
BLINK_SPEED		= 1.0				# Float in seconds, e.g. 0.5 for half a second

# Function to convert degrees fahrenheit to celsius
def FtoC(temp):
	return ((temp - 32) * (5/9))

# Function to convert degrees celsius to fahrenheit
def CtoF(temp):
	return ((temp * (9/5)) + 32)

# Initialize the LED strip
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness = LED_BRIGHTNESS, pixel_order = LED_ORDER, auto_write = False)

# Read the airports file to retrieve list of airports and use as order for LEDs
with open("/home/pi/METARMap/airports") as f:
	airports = f.readlines()
airports = [x.strip() for x in airports]

# Retrieve METAR from aviationweather.gov data server
# Details about parameters can be found here: https://www.aviationweather.gov/dataserver/example?datatype=metar
url = "https://www.aviationweather.gov/adds/dataserver_current/httpparam?dataSource=metars&requestType=retrieve&format=xml&hoursBeforeNow=5&mostRecentForEachStation=true&stationString=" + ",".join([item for item in airports if item != "NULL"])
print(url)

content = urllib.request.urlopen(url).read()

# Retrieve flying conditions from the service response and store in a dictionary for each airport
root = ET.fromstring(content)
conditionDict = { "": {"tempC" : 0, "dewpointC" : 0,} }
for metar in root.iter('METAR'):
	stationId = metar.find('station_id').text
	tempC = 0
	dewpointC = 0
	if metar.find('temp_c') is not None:
		tempC = float(metar.find('temp_c').text)
	if metar.find('dewpoint_c') is not None:
		dewpointC = float(metar.find('dewpoint_c').text)

	# Calculate weather values
	e = 6.11 * 10**((7.5 * dewpointC)/(237.3 + dewpointC))
	e_s = 6.11 * 10**((7.5 * tempC)/(237.3 + tempC))
	rh  = e/e_s * 100

	tempF = CtoF(tempC) 
	# hi = -42.379 + 2.04901523*tempF + 10.14333127*rh - .22475541*tempF*rh - .00683783*tempF*tempF - .05481717*rh*rh + .00122874*tempF*tempF*rh + .00085282*tempF*rh*rh - .00000199*tempF*tempF*rh*rh
	if tempF < 70:
		hi = -1
	elif tempF > 115:
		hi = 1000
	else:
		hi = 16.923 + 0.185212*tempF + 5.37941*rh - 0.100254*tempF*rh + 0.00941695*(tempF**2) + 0.00728898*(rh**2) + 0.000345372*(tempF**2)*rh - 0.000814971*tempF*(rh**2) + 0.0000102102*(tempF**2)*(rh**2) - 0.000038646*(tempF**3) + 0.0000291583*(rh**3) + 0.00000142721*(tempF**3)*rh + 0.000000197483*tempF*(rh**3) - 0.0000000218429*(tempF**3)*(rh**2) + 0.000000000843296*(tempF**2)*(rh**3) - 0.0000000000481975*(tempF**3)*(rh**3)
	t_w = tempC * numpy.arctan(0.151977 * (rh + 8.313659)**(1/2)) + numpy.arctan(tempC + rh) - numpy.arctan(rh - 1.676331) + 0.00391838 *(rh)**(3/2) * numpy.arctan(0.023101 * rh) - 4.686035
	WBGT = 0.7 * t_w + 0.3 * tempC

	# Round floats
	t_w = round(t_w * 10) / 10
	rh = round(rh * 10) / 10
	hi = round(hi*10) / 10
	WBGT = round(WBGT * 10) / 10

	print(stationId + "; T_c:" + str(tempC) + "; D_c:" + str(dewpointC) + "; RH:" + str(rh) +"; HI:" + str(hi) + "; T_w:" + str(t_w) + "; WBGT:" + str(WBGT))
	conditionDict[stationId] = { "tempC" : tempC, "dewpointC" : dewpointC, "RH" : rh, "heatIndex" : hi, "tempWet" : t_w, "WBGT" : WBGT }

# Setting LED colors based on weather conditions
flashCycle = False
while True:
	i = 0
	for airportcode in airports:
		# Skip NULL entries
		if airportcode == "NULL":
			i += 1
			continue

		color = COLOR_CLEAR
		conditions = conditionDict.get(airportcode, None)

		flash = True if flashCycle else False
		if conditions != None:
			# if ((tempC == 0) & (dewpointC == 0)):
			# 	color = COLOR_CLEAR
			# 	print("Error: temperature and/or dewpoint values unavailable.")
			if (flash and (conditions["heatIndex"] > HEAT_INDEX_THRESHOLD)):
				color = COLOR_HOT
			elif conditions["tempC"] < FtoC(0):
				color = COLOR_NEG
			elif conditions["tempC"] < FtoC(10):
				color = COLOR_0
			elif conditions["tempC"] < FtoC(20):
				color = COLOR_10
			elif conditions["tempC"] < FtoC(30):
				color = COLOR_20
			elif conditions["tempC"] < FtoC(40):
				color = COLOR_30
			elif conditions["tempC"] < FtoC(50):
				color = COLOR_40
			elif conditions["tempC"] < FtoC(60):
				color = COLOR_50
			elif conditions["tempC"] < FtoC(70):
				color = COLOR_60
			elif conditions["tempC"] < FtoC(80):
				color = COLOR_70
			elif conditions["tempC"] < FtoC(90):
				color = COLOR_80
			elif conditions["tempC"] < FtoC(100):
				color = COLOR_90
			elif conditions["tempC"] >= FtoC(100):
				color = COLOR_100
			else:
				color = COLOR_CLEAR
		pixels[i] = color
		i += 1

	# Update actual LEDs all at once
	pixels.show()

	# Switching between animation cycles
	time.sleep(BLINK_SPEED)
	flashCycle = False if flashCycle else True

print()
print("Done")
