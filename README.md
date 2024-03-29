# Badge Labortage 2021

![assembled badge](img/badge-lt21.jpg)

## Idea: based on Swag Badge

The idea for this year's Labor badge is based on the Swag Badge from the
[Open Hardware Miniconf at linux.conf.au 2021](
http://www.openhardwareconf.org/wiki/SwagBadge2021).

![Swag badge](
http://www.openhardwareconf.org/images/thumb/e/e7/Swag_badge_render_2020-09-30.jpg/360px-Swag_badge_render_2020-09-30.jpg)

They also released a DIY version named [Dag Badge](
http://www.openhardwareconf.org/wiki/Swagbadge2021_Dagbadge) as well as the
[Swag Badge schematics](https://github.com/CCHS-Melbourne/Swag-Badge).

## What?

You can do [fun things](https://mastodon.social/@CyReVolt/106513500102546977)
with this badge.
We made a basic kit as we sell it, with optional extras.

This is in part for educational purposes, so people can try different things,
e.g., discover that I2C needs different addresses or separate buses vs SPI
being controlled via active low _select_ pins.
The top area has holes for prototyping, not connected to anything.

### Basic kit

- power and system LEDs
- 2 OLED screens on I2C (top)
- 2 buttons
- double pin rows + ESP32 D1 mini board

### Extras

- 2 color screens on SPI
- 2 thumb sticks with buttons and x,y axis
- 2 expansion ports with I2C and DAC-capable GPIOs (top left+right)

## PCB

This is our own PCB design. We will offer a basic kit with the PCB itself, the
ESP32 D1 Mini board, 2 OLED displays, and 2 push buttons, to keep it simple and
inexpensive. Anyone can purchase the additional parts if they like and we may
have some left over from testing, and of course, feel free to fork and rework
the PCB as you like, print it yourself, file PRs, or just leave some feedback.

Size (rounded): 94mm x 130mm

![Badge](badge.png)

See the [schematics](hw/schematics.pdf) for details.

## ESP32 D1 Mini

The data sheet and documentation for the ESP32-WROOM-32 is [publicly available](
https://www.espressif.com/sites/default/files/documentation/esp32-wroom-32_datasheet_en.pdf).

It includes schematics and application notes.

### Further Documents

- [all technical docs](https://www.espressif.com/en/support/documents/technical-documents)
- [ESP32 technical reference manual](
  https://www.espressif.com/sites/default/files/documentation/esp32_technical_reference_manual_en.pdf)
- [ESP32 general datasheet](
  https://www.espressif.com/sites/default/files/documentation/esp32_datasheet_en.pdf)

### Buy

[https://www.az-delivery.de/products/esp32-d1-mini](
https://www.az-delivery.de/products/esp32-d1-mini)

### Pinout

![ESP32 D1 Mini Pinout](
https://www.bastelgarage.ch/image/catalog/Artikel/420571-420580/420571-Pinout.jpg)

The [ESP32 has VDET pins](https://www.esp32.com/viewtopic.php?t=187) which can
be used for ADC.

#### MH-ET LIVE MiniKit

**NOTE**: At Labortage 2021, we sold badges with the MH-ET LIVE MiniKit, because
it was a cheap option and easily available, unlike the otherwise preferred board
"ESP32 D1 Mini NodeMCU". It has some quirks, but is generally fine to use.

We have bridged button B (right) to GPIO0, so you can press it for flashing or
otherwise triggering the "boot option" as described in the WROOM-32 datasheet.

- [forum with resources overview](
https://forum.mhetlive.com/topic/8/mh-et-live-minikit-for-esp32)
- [repo with sample files for Arduino](
https://github.com/MHEtLive/ESP32-MINI-KIT)
- [issue: schematics not fully accurate](
https://github.com/MHEtLive/ESP32-MINI-KIT/issues/3)
- [issue: RX/TX in top right are swapped](
https://github.com/MHEtLive/ESP32-MINI-KIT/issues/7)

### Firmware

Use the `Makefile` to clear the SPI flash and write an image to it:

```sh
make FW=firmware-image.bin erase flash
```

You can pass down parameters. For further options, please look at `Makefile`.

**NOTE: One common board is the MH-ET LIVE ESP32 MiniKit. In order to flash it,
you need to short `GPIO0` to `GND` and use the assigned /dev/ttyACM{n} device.**

#### [das-labor/badge-2021-rs](https://github.com/das-labor/badge-2021-rs)

We have started to write our own bare firmware in Rust. :crab:

It is non-std and based on [esp-rs](https://esp-rs.github.io/book/).

#### [MicroPython](https://micropython.org/download/esp32/)

It's in beta and we were having trouble getting MQTT and WiFi to work reliably.

Use [`ampy`](https://github.com/scientifichackers/ampy) to upload scripts. On
many OS distributions, you can find a package for it.

#### [NodeMCU](https://nodemcu.readthedocs.io/en/dev-esp32/)

The ESP32 variant is also still in beta on NodeMCU, though may do better than MicroPython.
We haven't tested it too much yet, but it does boot up thus far and MQTT worked okay.

Use [`nodemcu-tool`](https://github.com/AndiDittrich/NodeMCU-Tool) to upload
scripts. If you are using Arch Linux, you can use the [package from the AUR](
https://aur.archlinux.org/cgit/aur.git/tree/PKGBUILD?h=nodemcu-tool). Otherwise,
use the `PKGBUILD` as a reference for building it; mind that you may need to
rebuild the native modules.

Follow the [build instructions](https://nodemcu.readthedocs.io/en/dev-esp32/build/)
for full customization or use a [prebuilt image from the cloud build service](
https://hostile.education/nodemcu-dev-esp32-13-modules-2021-10-17-00-22-29-float.bin).

#### 9p support

Try out [a small libstyx implementation suitable for use on ESP32](
https://github.com/bhgv/listyx2-9p-C-lib-and-plugins).

See also the more recent [NinePea](https://github.com/echoline/NinePea).

**TODO**: See if you can wire it up with [`cpu`](
https://github.com/u-root/cpu) to enable speedier driver development,
e.g., using a related ESP32 board with an ethernet port, or attach
one to the badge even.

## Buttons

There are many suitable and colorful [6x6 buttons, tall and high](
https://www.amazon.de/-/en/dp/B087R5XYJW/), though not as nice to
press. We went with the larger [12x12 retro arcade style tactile
push buttons](https://www.amazon.de/-/en/dp/B07WPBQXJ9) instead.

We have routed the buttons to the pins `IO0` and `IO2`.

## OLED I2C Display

**Note**: On the back, we need to solder a bridge on *one* display
in order to change its address, so we can use both on the same bus.

The module is based on the SSD1306. See also the [data sheet](
https://cdn-shop.adafruit.com/datasheets/SSD1306.pdf) and
![schematics for a similar design](
https://cdn-learn.adafruit.com/assets/assets/000/093/884/original/adafruit_products_0-96in_OLED_sch.png).

### Buy

[https://www.az-delivery.de/en/products/0-96zolldisplay](
https://www.az-delivery.de/en/products/0-96zolldisplay)

### Front

![display front](
https://user-images.githubusercontent.com/33422878/37134592-383bf65a-22d4-11e8-8d32-1a8aad043f5f.png)

### Back

![display back](
https://user-images.githubusercontent.com/33422878/37134695-a056b0cc-22d4-11e8-8a5f-b13621fd9ad1.png)

## Joysticks / Thumbsticks

PS2 joysticks and corresponding caps are [available from Amazon](
https://www.amazon.de/-/en/Replacement-DualShock-Controller-Playstation-Screwdriver/dp/B07R7TM177/)
and probably other sources as well.

The Freetronics Kicad library [has a model for it](
https://github.com/freetronics/freetronics_kicad_library/blob/master/freetronics_footprints.pretty/JOYSTICK_W_BUTTON.kicad_mod).

They have two potentiometers for the two dimensions each, so we assign GPIO pins
to them:

|  function  | left | right |
| ---------- | ---- | ----- |
|   X axis   | IO33 |  IO32 |
|   Y axis   | IO34 |  IO35 |
|   button   | IO5  |  IO12 |

## Other ESP32 Boards

[https://www.mischianti.org/2020/05/30/esp32-pinout-specs-and-arduino-ide-configuration-part-1/](
https://www.mischianti.org/2020/05/30/esp32-pinout-specs-and-arduino-ide-configuration-part-1/)

## Demo

[MicroPython SSD1306 OLED Display Scroll and Shapes](
https://randomnerdtutorials.com/micropython-ssd1306-oled-scroll-shapes-esp32-esp8266/)

### Sources

- [ssd1306.py](
  https://github.com/RuiSantosdotme/ESP-MicroPython/raw/master/code/Others/OLED/ssd1306.py)
- [screen_scroll.py](
https://github.com/RuiSantosdotme/Random-Nerd-Tutorials/raw/master/Projects/ESP-MicroPython/oled/screen_scroll.py)
