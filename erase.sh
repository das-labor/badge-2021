#!/bin/sh

esptool.py --chip esp32 --port /dev/ttyUSB0 erase_flash
