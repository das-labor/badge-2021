# Adapted from
# https://github.com/boochow/MicroPython-ST7735/blob/master/tftbmp.py
# and
# https://randomnerdtutorials.com/esp32-esp8266-analog-readings-micropython/

from machine import Pin, ADC, SPI
import time
from ST7735 import TFT, TFTColor

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
  time.sleep_us(500)
