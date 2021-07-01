# Adapted from
# https://github.com/boochow/MicroPython-ST7735/blob/master/tftbmp.py
# and
# https://randomnerdtutorials.com/esp32-esp8266-analog-readings-micropython/

from machine import Pin, ADC, SPI
import time
from ST7735 import TFT, TFTColor

# joystick l h
jlh = ADC(Pin(32))
jlh.atten(ADC.ATTN_11DB)       #Full range: 3.3v

# joystick l v
jlv = ADC(Pin(34))
jlv.atten(ADC.ATTN_11DB)       #Full range: 3.3v

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
time.sleep_us(50000)
tft1.rect([26,1], [80,160], TFT.PURPLE)
tft1.fillrect([27,2], [20,20], TFTColor(42, 111, 123))
tft1.fillrect([40,50], [25,15], TFT.RED)
tft1.fillrect([50,70], [25,15], TFT.BLUE)
tft1.fillrect([60,90], [25,15], TFT.GREEN)
tft1.fillrect([85,140], [20,20], TFTColor(123, 111, 42))

# tft2
time.sleep_us(50000)
tft2.rect([26,1], [80,160], TFT.PURPLE)
tft2.fillrect([27,2], [20,20], TFTColor(42, 111, 123))
tft2.fillrect([40,50], [25,15], TFT.GREEN)
tft2.fillrect([50,70], [25,15], TFT.RED)
tft2.fillrect([60,90], [25,15], TFT.BLUE)
tft2.fillrect([85,140], [20,20], TFTColor(123, 111, 42))

time.sleep_us(500000)

x = 50
y = 50

while True:
  xd = jlh.read()
  yd = jlv.read()
  print(xd)
  print(yd)
  x = x + (xd-1580) / 100
  if x < 27:
    x = 27
  if x > 85:
    x = 85
  y = y + (yd-1770) / 100
  if y < 2:
    y = 2
  if y > 140:
    y = 140
  tft2.fill(TFT.BLACK)
  tft2.rect([26,1], [80,160], TFT.PURPLE)
  tft2.fillrect([x,y], [20,20], TFT.BLUE)
  time.sleep_us(500)
