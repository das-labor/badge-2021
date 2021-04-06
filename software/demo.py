import time
import math
from emulator import SSD1306_I2C

def handle_px(t, x, y):
    v = math.sin(1*(0.5*x*math.sin(t/2) +
                    0.5*y*math.cos(t/3)) + t)
    # -1 < sin() < +1
    # therefore correct the value and bring into range [0, 1]
    v = (v+1.0) / 2.0
    return v

i = 0
oled = SSD1306_I2C(addr=0x78)

while True:
    t = time.time()
    for y in range(oled.height):
        for x in range(oled.width):
            v = int(handle_px(t, x, y) * 120)
            oled.pixel(x, y, (v,v,0))

    oled.hline(0, oled.height*(math.sin(3*t)+1)//2, oled.width,
        (100,0,200))

    oled.vline(2*i,0,oled.height, (100,0,200))
    oled.text("Das Labor", i, 10, (100,200,200))
    oled.text("Badge 2021", i+20, 30, (0,200,100))

    oled.rect(i+18, 30, 65, 10, (200,200,200))
    #oled.fill_rect(i+18, 45, 65, 5, (200,200,200))
    #oled.blit(oled, 10,10)
    #oled.scroll(i,i)
    i = -80 if i+1>oled.width else i+1
    oled.show()

    time.sleep(0.01)
