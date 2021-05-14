# Adapted from
# https://github.com/boochow/MicroPython-ST7735/blob/master/tftbmp.py

from machine import Pin, SPI
import time
from ST7735 import TFT, TFTColor

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
tft = TFT(spi, aDC=16, aReset=17, aCS=23)

tft.initr()
tft.rgb(True)
tft.invertcolor(True)
tft.fill(TFT.BLACK)
time.sleep_us(50000)
tft.rect([26,1], [80,160], TFT.PURPLE)
tft.fillrect([27,2], [20,20], TFTColor(42, 111, 123))
tft.fillrect([40,50], [25,15], TFT.GREEN)
tft.fillrect([50,70], [25,15], TFT.RED)
tft.fillrect([60,90], [25,15], TFT.BLUE)
tft.fillrect([85,140], [20,20], TFTColor(123, 111, 42))
