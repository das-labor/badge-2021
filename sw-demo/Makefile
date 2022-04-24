#!/bin/sh

AMPY := ampy
PORT := /dev/ttyACM0

upload:
	$(AMPY) -p $(PORT) put boot.py
	$(AMPY) -p $(PORT) put ssd1306.py
	$(AMPY) -p $(PORT) put i2c_scroll.py
	$(AMPY) -p $(PORT) put ST7735.py
	$(AMPY) -p $(PORT) put spi_rects.py
	$(AMPY) -p $(PORT) put tft.py
