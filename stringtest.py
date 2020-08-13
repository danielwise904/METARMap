import board
import neopixel
pixels = neopixel.NeoPixel(board.D18,150)
i = 0
brightness = 0.1
while i <= 149:
    pixels[i] = (255*brightness,255*brightness,255*brightness)
    pixels.show
    print("LED " + str(i+1))
    input("Press enter to continue...")
    pixels[i] = (0,0,0)
    pixels.show
    i = i + 1
    if i == 149:
         i = 0