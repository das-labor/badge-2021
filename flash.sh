#!/bin/sh

# --port /dev/ttyUSB0 \
esptool.py \
  --chip esp32 \
  --baud 460800 write_flash \
  -z 0x1000 \
  $@
