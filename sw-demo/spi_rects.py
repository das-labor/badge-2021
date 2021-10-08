# Adapted from
# https://github.com/boochow/MicroPython-ST7735/blob/master/tftbmp.py
# and
# https://randomnerdtutorials.com/esp32-esp8266-analog-readings-micropython/

from machine import Pin, ADC, I2C, SPI
from time import sleep, sleep_us
from ST7735 import TFT, TFTColor
import ssd1306

button_A = Pin(0, Pin.IN, Pin.PULL_UP)
button_B = Pin(2, Pin.IN, Pin.PULL_UP)

led = Pin(4, Pin.OUT)
led_state = False

print("I2C display scroller")
# ESP32 Pin assignment
i2c = I2C(-1, scl=Pin(22), sda=Pin(21))

oled_width = 128
oled_height = 64
oled1 = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
oled2 = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c, 0x3d)

screen1 = [
        [0, 10 , "== LNI  2021 =="],
        [0, 42 , "woop woop woop!"]
]
screen2 = [
        [0, 16, "> COViD sucks <"],
        [0, 16, " pew! pew! pew!"]
]
screen3 = [
        [0, 40, "|||||||||||||||"],
        [0, 32, "-- Das Labor --"]
]

# Scroll in screen horizontally from left to right
def scroll_in_screen(screen):
  for i in range (0, oled_width+1, 4):
    oled1.text(screen[0][2], -oled_width+i, screen[0][1])
    oled2.text(screen[1][2], -oled_width+i, screen[1][1])
    oled1.show()
    oled2.show()
    if i!= oled_width:
      oled1.fill(0)
      oled2.fill(0)

# Scroll out screen horizontally from left to right
def scroll_out_screen(speed):
  for i in range ((oled_width+1)/speed):
    for j in range (oled_height):
      oled1.pixel(i, j, 0)
    oled1.scroll(speed,0)
    oled1.show()

# Continuous horizontal scroll
def scroll_screen_in_out(screen):
  for i in range (0, (oled_width+4)/4, 1):
    for line in screen:
      oled1.text(line[2], -oled_width+i*8, line[1])
    oled1.show()
    if i<= oled_width/4:
      oled1.fill(0)

# Scroll in screen vertically
def scroll_in_screen_v(screen):
  for i in range (0, (oled_height+1), 1):
    for line in screen:
      oled1.text(line[2], line[0], -oled_height+i+line[1])
    oled1.show()
    if i!= oled_height:
      oled1.fill(0)

# Scroll out screen vertically
def scroll_out_screen_v(speed):
  for i in range ((oled_height+1)/speed):
    for j in range (oled_width):
      oled1.pixel(j, i, 0)
    oled1.scroll(0,speed)
    oled1.show()

scroll_in_screen(screen2)
sleep(2)
scroll_out_screen(4)
scroll_in_screen_v(screen3)
sleep(2)
scroll_out_screen_v(4)

# joystick left horizontal
jlh = ADC(Pin(33))
jlh.atten(ADC.ATTN_11DB)       #Full range: 3.3v
# joystick left vertical
jlv = ADC(Pin(34))
jlv.atten(ADC.ATTN_11DB)       #Full range: 3.3v

# joystick right horinzontal
jrh = ADC(Pin(32))
jrh.atten(ADC.ATTN_11DB)       #Full range: 3.3v
# joystick right vertical
jrv = ADC(Pin(35))
jrv.atten(ADC.ATTN_11DB)       #Full range: 3.3v

## ADC.WIDTH_9BIT: range 0 to 511
## ADC.WIDTH_10BIT: range 0 to 1023
## ADC.WIDTH_11BIT: range 0 to 2047
## ADC.WIDTH_12BIT: range 0 to 4095

# from https://forum.micropython.org/viewtopic.php?t=5677
# is it any better?
# spi = SPI(2, baudrate=20000000, sck=Pin(18), mosi=Pin(23), miso=Pin(19))

print("SPI TFT display rectangles")
spi = SPI(
   2,
   baudrate=24000000,
   polarity=0,
   phase=0,
   sck=Pin(14),
   mosi=Pin(13),
   miso=Pin(12)
)

# tft = TFT(spi, aDC=27, aReset=26, aCS=14)
tft1 = TFT(spi, aDC=16, aReset=17, aCS=23)
tft2 = TFT(spi, aDC=16, aReset=19, aCS=18)

## init
tft1.initr()
tft1.rgb(True)
tft1.invertcolor(True)
tft1.fill(TFT.BLACK)
tft2.initr()
tft2.rgb(True)
tft2.invertcolor(True)
tft2.fill(TFT.BLACK)

# tft1
tft1.rect([26,1], [80,160], TFT.PURPLE)
tft1.fillrect([27,2], [20,20], TFTColor(42, 111, 123))
tft1.fillrect([40,50], [25,15], TFT.RED)
tft1.fillrect([50,70], [25,15], TFT.BLUE)
tft1.fillrect([60,90], [25,15], TFT.GREEN)
tft1.fillrect([85,140], [20,20], TFTColor(123, 111, 42))

# tft2
tft2.rect([26,1], [80,160], TFT.PURPLE)
tft2.fillrect([27,2], [20,20], TFTColor(42, 111, 123))
tft2.fillrect([40,50], [25,15], TFT.GREEN)
tft2.fillrect([50,70], [25,15], TFT.RED)
tft2.fillrect([60,90], [25,15], TFT.BLUE)
tft2.fillrect([85,140], [20,20], TFTColor(123, 111, 42))

sleep_us(500000)

# left pos and joystick offset
xl = 50
yl = 50
hl_off = -195 # TODO
vl_off = -384 # TODO

# right pos and joystick offset
xr = 50
yr = 50
hr_off = -195
vr_off = -384

while True:
  xrr = jrh.read() #
  yrr = jrv.read() #
  xrd = (xrr - (2048 + hr_off)) / 100
  yrd = (yrr - (2048 + vr_off)) / 100
  xlr = jlh.read() #  15.48  1853.52  4079.52
  ylr = jlv.read() #  17.48  1664.52  4077.52
  xld = (xlr - (2048 + hl_off)) / 100
  yld = (ylr - (2048 + vl_off)) / 100
  if abs(xld) > 3 or abs(yld) > 3:
      xl = xl - xld # joystick is inverted
      yl = yl - yld # joystick is inverted
      if xl < 27:
        xl = 27
      if xl > 85:
        xl = 85
      if yl < 2:
        yl = 2
      if yl > 140:
        yl = 140
      tft1.fill(TFT.BLACK)
      tft1.rect([26,1], [80,160], TFT.PURPLE)
      tft1.fillrect([xl,yl], [20,20], TFT.GREEN)
  if abs(xrd) > 3 or abs(yrd) > 3:
      xr = xr + xrd
      yr = yr + yrd
      if xr < 27:
        xr = 27
      if xr > 85:
        xr = 85
      if yr < 2:
        yr = 2
      if yr > 140:
        yr = 140
      tft2.fill(TFT.BLACK)
      tft2.rect([26,1], [80,160], TFT.PURPLE)
      tft2.fillrect([xr,yr], [20,20], TFT.BLUE)

  if not button_A.value():
      print("Button A")
      led_state = not led_state
      led.value(1 if led_state else 0)

  if not button_B.value():
      print("Button B")
      scroll_screen_in_out(screen1)

  sleep_us(500)
