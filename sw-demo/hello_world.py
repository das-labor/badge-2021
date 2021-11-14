import time
import math

from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from time import sleep

# ESP32 Pin assignment
i2c = I2C(-1, scl=Pin(22), sda=Pin(21))

oled_width = 128
oled_height = 64

print('Init displays')
oled1 = SSD1306_I2C(oled_width, oled_height, i2c, 0x3c)
oled2 = SSD1306_I2C(oled_width, oled_height, i2c, 0x3d)

print('init LED')
led = Pin(4, Pin.OUT)

print('init buttons')
btn_left = Pin(0, Pin.IN, Pin.PULL_UP)
btn_right = Pin(2, Pin.IN, Pin.PULL_UP)

BLACK = 0
WHITE = 1

i = 0
x, y = 0, 60
while True:
    oled1.fill(BLACK)
    oled2.fill(BLACK)

    # show button state
    dx = 0
    led.off()
    if btn_left.value()==0:  
        oled1.text("Left Button", 0, 20)
        dx = -4
        led.on()
    if btn_right.value()==0: 
        oled2.text("Right Button", 0, 20)
        dx = +4
        led.on()

    x += dx
    x = min(x, 2 * oled_width - 1)
    x = max(x, 0)

    # show some text
    oled1.text("Hello", i, 10)
    oled2.text("World", i, 10)

    # draw pixel into left or right display
    if 0 <= x <= oled1.width:
        oled1.pixel(x, y, WHITE)
    else:
        oled2.pixel(x-oled_width, y, WHITE)

    # show displays
    oled1.show()
    oled2.show()

    i = -80 if i+1>oled1.width else i+2

