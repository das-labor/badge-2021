#!/bin/sh

_PORT=/dev/ttyACM3

ampy -p $_PORT put boot.py
ampy -p $_PORT put ssd1306.py
ampy -p $_PORT put i2c_scroll.py
ampy -p $_PORT put ST7735.py
ampy -p $_PORT put spi_rects.py
ampy -p $_PORT put tft.py
