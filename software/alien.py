# inspired by
# https://hackaday.com/2021/04/13/alien-art-drawn-with-surprisingly-simple-math/

from emulator import SSD1306_I2C
import time

BLACK = 0
WHITE = 1
SLEEPTIME = 0.05 # seconds to wait between updates

oled = SSD1306_I2C(addr=0x78)

offset, direction = 1, +1
while True:
    offset += direction
    if offset >= 9: direction=-1
    elif offset<0: direction= +1

    for y in range(oled.height):
        for x in range(oled.width):
            v = (x ^ y ) % 9
            col = BLACK if v<offset else WHITE
            oled.pixel(x,y,col)

    oled.show()
    time.sleep(SLEEPTIME)
