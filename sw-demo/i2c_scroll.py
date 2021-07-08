# Complete project details at https://RandomNerdTutorials.com/micropython-ssd1306-oled-scroll-shapes-esp32-esp8266/

from machine import Pin, I2C
import ssd1306
from time import sleep

print("I2C display scroller")

# ESP32 Pin assignment
i2c = I2C(-1, scl=Pin(22), sda=Pin(21))

# ESP8266 Pin assignment
#i2c = I2C(-1, scl=Pin(5), sda=Pin(4))

oled_width = 128
oled_height = 64
oled = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c)
oled2 = ssd1306.SSD1306_I2C(oled_width, oled_height, i2c, 0x3d)

screen1 = [
        [0, 0 , "== LNI  2021 =="],
        [0, 0 , "woop woop woop!"]
]
screen2 = [
        [0, 16, "> COViD sucks <"],
        [0, 16, " pew! pew! pew!"]
]
screen3 = [
        [0, 40, "|||||||||||||||"],
        [0, 32, "-- Das Labor --"]
]

# Scroll in screen horizontally from left to right
def scroll_in_screen(screen):
  for i in range (0, oled_width+1, 4):
    oled.text(screen[0][2], -oled_width+i, screen[0][1])
    oled2.text(screen[1][2], -oled_width+i, screen[1][1])
    oled.show()
    oled2.show()
    if i!= oled_width:
      oled.fill(0)
      oled2.fill(0)

# Scroll out screen horizontally from left to right
def scroll_out_screen(speed):
  for i in range ((oled_width+1)/speed):
    for j in range (oled_height):
      oled.pixel(i, j, 0)
    oled.scroll(speed,0)
    oled.show()

# Continuous horizontal scroll
def scroll_screen_in_out(screen):
  for i in range (0, (oled_width+1)*2, 1):
    for line in screen:
      oled.text(line[2], -oled_width+i, line[1])
    oled.show()
    if i!= oled_width:
      oled.fill(0)

# Scroll in screen vertically
def scroll_in_screen_v(screen):
  for i in range (0, (oled_height+1), 1):
    for line in screen:
      oled.text(line[2], line[0], -oled_height+i+line[1])
    oled.show()
    if i!= oled_height:
      oled.fill(0)

# Scroll out screen vertically
def scroll_out_screen_v(speed):
  for i in range ((oled_height+1)/speed):
    for j in range (oled_width):
      oled.pixel(j, i, 0)
    oled.scroll(0,speed)
    oled.show()

# Continous vertical scroll
def scroll_screen_in_out_v(screen):
  for i in range (0, (oled_height*2+1), 1):
    for line in screen:
      oled.text(line[2], line[0], -oled_height+i+line[1])
    oled.show()
    oled.show()
    if i!= oled_height:
      oled.fill(0)

def loop():
# # Scroll in, stop, scroll out (horizontal)
# scroll_in_screen(screen1)
# sleep(2)
# scroll_out_screen(4)

  scroll_in_screen(screen2)
  sleep(2)
  scroll_out_screen(4)

# scroll_in_screen(screen3)
# sleep(2)
# scroll_out_screen(4)

# # Continuous horizontal scroll
# scroll_screen_in_out(screen1)
# scroll_screen_in_out(screen2)
# scroll_screen_in_out(screen3)

# # Scroll in, stop, scroll out (vertical)
# scroll_in_screen_v(screen1)
# sleep(2)
# scroll_out_screen_v(4)

# scroll_in_screen_v(screen2)
# sleep(2)
# scroll_out_screen_v(4)

  scroll_in_screen_v(screen3)
  sleep(2)
  scroll_out_screen_v(4)

# # Continuous verticall scroll
# scroll_screen_in_out_v(screen1)
# scroll_screen_in_out_v(screen2)
# scroll_screen_in_out_v(screen3)


loop()
