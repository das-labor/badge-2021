#!/bin/sh

_PORT=/dev/ttyACM0

ampy -p $_PORT put boot.py
ampy -p $_PORT put ssd1306.py
ampy -p $_PORT put hw_test.py
