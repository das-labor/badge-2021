from machine import Pin, ADC, SPI
import st7789py

button_A = Pin(39, Pin.IN)
button_B = Pin(2, Pin.IN, Pin.PULL_UP)
button_JA = Pin(5, Pin.IN, Pin.PULL_UP)
button_JB = Pin(12, Pin.IN, Pin.PULL_UP)

led = Pin(4, Pin.OUT)
led_state = False

spi = SPI(
   1,
   baudrate=40000000,
   polarity=1,
   phase=0,
   sck=Pin(14),
   mosi=Pin(13),
   miso=Pin(12)
)

dc    = Pin(16, Pin.OUT)
reset = Pin(17, Pin.OUT)

display = st7789py.ST7789(spi, 240, 240, reset=reset, dc=dc)

print("SPI TFT display init")
display.init()

while True:
    # TODO: GPIO pins 34-39 do not have a pull-up resistor :(
    # see https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/peripherals/gpio.html
    #if not button_A.value():
    #    display.fill_rect(50, 70, 25, 25, st7789py.YELLOW)
    #    print("Button A")

    if not button_B.value():
        display.fill_rect(80, 110, 35, 75, st7789py.BLUE)
        print("Button B")
        led_state = not led_state
        led.value(1 if led_state else 0)

    if not button_JA.value():
        display.fill_rect(20, 40, 15, 15, st7789py.RED)
        print("Joystick A")

    if not button_JB.value():
        display.fill_rect(160, 110, 45, 95, st7789py.GREEN)
        print("Joystick B")
