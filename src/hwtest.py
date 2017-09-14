from neopixel import NeoPixel
import machine as m
import time

SWITCHES_PINS = [ 12, 13, 14, 17 ]
LEDS_PINS = [ 32, 33, 34, 35 ]
NEOPIXEL_SIZE = 64*2+18

d = NeoPixel(m.Pin(18, m.Pin.OUT), NEOPIXEL_SIZE)
d.timing = 1

switches = [ m.Pin(p, m.Pin.IN) for p in SWITCHES_PINS ]
leds = [ m.Pin(p, m.Pin.OUT) for p in LEDS_PINS ]

while True:
    for i in range(NEOPIXEL_SIZE):
        # check buttons
        for switch in switches:
            if switch.value():
                print("Switch ON: " + str(switch))

        # check leds
        for led in leds:
            led.value(0 if led.value() else 1)

        # clear board
        for j in range(NEOPIXEL_SIZE):
            d[j] = (0, 0, 0)

        d[i] = (100, 0, 100)
        d.write()

        # wait for user input
        # while switches[0].value() == 0:
        #     pass

        time.sleep_ms(500)
