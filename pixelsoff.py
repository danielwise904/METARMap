import board
import neopixel

pixels = neopixel.NeoPixel(board.D18, 150)

pixels.deinit()

print("LEDs off")
