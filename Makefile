# The name of the file to flash that you downloaded, e.g., from MicroPython.
FW := firmware.bin
# Some distros call the binary simply `esptool`.
ESPTOOL_BIN := esptool.py
ESPTOOL_PARAMS := --chip esp32 --baud 460800
# The port may also be `/dev/ttyUSB0`, depending on your board.
PORT := /dev/ttyACM0

ESPTOOL := $(ESPTOOL_BIN) --port $(PORT) $(ESPTOOL_PARAMS)

flash:
	$(ESPTOOL) write_flash --flash_mode dio --flash_freq 40m --flash_size 4MB \
		-z 0x1000 $(FW)

erase:
	$(ESPTOOL) erase_flash

info:
	$(ESPTOOL) chip_id
	$(ESPTOOL) flash_id
	$(ESPTOOL) get_security_info

fwinfo:
	$(ESPTOOL) image_info $(FW)
