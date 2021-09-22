#!/bin/sh

# --port /dev/ttyUSB0 \
esptool.py \
  --chip esp32 \
  --baud 460800 write_flash \
  --flash_mode dio \
  --flash_freq 40m \
  --flash_size 4MB \
  -z 0x1000 \
  $@
