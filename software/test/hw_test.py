# HW test sequence for badge-2021 REV 2

from machine import Pin
from time import sleep


button_A = Pin(0, Pin.IN, Pin.PULL_UP)
button_B = Pin(2, Pin.IN, Pin.PULL_UP)

led = Pin(4, Pin.OUT)

dac_1 = Pin(26, Pin.OUT)
dac_2 = Pin(25, Pin.OUT)

i2c_sda = Pin(21, Pin.OUT)
i2c_scl = Pin(22, Pin.OUT)

spi_clk = Pin(14, Pin.OUT)
spi_mosi = Pin(13, Pin.OUT)

spi_cs_1 = Pin(23, Pin.OUT)
spi_cs_2 = Pin(18, Pin.OUT)

disp_1_rst = Pin(17, Pin.OUT)
disp_2_rst = Pin(19, Pin.OUT)

j_button_A = Pin(5, Pin.OUT)
j_button_B = Pin(12, Pin.OUT)

def loop():

    print("START TEST")

    cnt = 0


    # --- LOOP ---

    while True:
        if button_A.value() == 0:
            if cnt > 0:
                cnt = cnt-1

        if button_B.value() == 0:
            if cnt < 13:
                cnt = cnt+1
            
        print("Counter:")
        print(cnt)

        # --- RESET GPIO ---
        led.value(0)
        
        dac_1.value(0)
        dac_2.value(0)
        
        i2c_sda.value(0)
        i2c_scl.value(0)

        spi_clk.value(0)
        spi_mosi.value(0)
        spi_cs_1.value(0)
        spi_cs_2.value(0)

        disp_1_rst.value(0)
        disp_2_rst.value(0)

        j_button_A.value(0)
        j_button_B.value(0)

        # --- Iterate through GPIO ---
        if cnt == 1:
            print("LED")
            led.value(1)

        if cnt == 2:
            print("DAC 1")
            dac_1.value(1)         

        if cnt == 3:
            print("DAC 2")
            dac_2.value(1)
        
        if cnt == 4:
            print("I2C SDA")
            i2c_sda.value(1)

        if cnt == 5:
            print("I2C SCL")
            i2c_scl.value(1)

        if cnt == 6:
            print("SPI CLK")
            spi_clk.value(1)

        if cnt == 7:
            print("SPI MOSI")
            spi_mosi.value(1)

        if cnt == 8:
            print("SPI CS 1")
            spi_cs_1.value(1)

        if cnt == 9:
            print("SPI CS 2")
            spi_cs_2.value(1)

        if cnt == 10:
            print("DISPLAY 1 RST")
            disp_1_rst.value(1)

        if cnt == 11:
            print("DISPLAY 2 RST")
            disp_2_rst.value(1)

        if cnt == 12:
            print("J Button A")
            j_button_A.value(1)

        if cnt == 13:
            print("J Button B")
            j_button_B.value(1)
            
        sleep(1)
    
loop()
