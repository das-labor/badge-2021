import time
import math
from emulator import SSD1306_I2C

BLACK = 0
WHITE = 1

def handle_px(t, x, y):
    v = math.sin(1*(0.5*x*math.sin(t/2) +
                    0.5*y*math.cos(t/3)) + t)
    # -1 < sin() < +1
    # therefore correct the value and bring into range [0, 1]
    v = (v+1.0) / 2.0
    if v>0.5: return WHITE
    else: return BLACK

i = 0
oled = SSD1306_I2C(addr=0x78)
oled.contrast(200)

while True:
    t = time.time()
    oled.fill_rect(0,0, oled.width,oled.height, BLACK)
    for y in range(oled.height//2,oled.height):
        for x in range(oled.width):
            v = handle_px(t, x, y)
            oled.pixel(x, y, v)

    oled.hline(0, oled.height//2*(math.sin(3*t)+1)//2, oled.width, WHITE)

    oled.vline(2*i,0,oled.height//2, BLACK)
    oled.text("Das Labor", i, 0, WHITE)
    oled.text("Badge 2021", i+20, 10, WHITE)

    oled.rect(i+18, 10, 65, 10, WHITE)
    #oled.blit(oled, 10,10)
    #oled.scroll(i,i)
    i = -80 if i+1>oled.width else i+1
    oled.show()

    time.sleep(0.01)
