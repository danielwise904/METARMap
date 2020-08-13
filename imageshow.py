#!/usr/bin/env python3

import urllib.request
import xml.etree.ElementTree as ET
import board
import neopixel
import time

# NeoPixel LED Configuration
LED_COUNT			= 150				# Number of LED pixels.
LED_PIN				= board.D18			# GPIO pin connected to the pixels (18 is PCM).
LED_BRIGHTNESS		= 0.4				# Float from 0.0 (min) to 1.0 (max)
LED_ORDER			= neopixel.GRB			# Strip type and colour ordering

GREEN			= (255,0,0)
BLUE			= (0,0,255)	
RED				= (0,255,0)
MAGENTA			= (0,125,125)
BLACK			= (0,0,0)
WHITE			= (255,255,255)

class Switch(dict):
    def __getitem__(self, item):
        for key in self.keys():                   # iterate over the intervals
            if item in key:                       # if the argument is part of that interval
                return super().__getitem__(key)   # return its associated value
        raise KeyError(item)    


# Initialize the LED strip
pixels = neopixel.NeoPixel(LED_PIN, LED_COUNT, brightness = LED_BRIGHTNESS, pixel_order = LED_ORDER, auto_write = False)

# Define color layout (GRB)
color = Switch({
range(1,151): (102,255,204)

	})

for i in range(LED_COUNT):
	pixels[i] = color[i + 1]

pixels.show()

print()
print("Done")
