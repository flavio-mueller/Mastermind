from neopixel import NeoPixel
from machine import Pin
import random
import time

numPixel = 64
neoPin = Pin(18,Pin.OUT)

neoPixel = NeoPixel(neoPin, numPixel)

button1 = Pin(12, Pin.IN)
button2 = Pin(13, Pin.IN)
button3 = Pin(14, Pin.IN)

button1LED = Pin(25, Pin.OUT)
button2LED = Pin(26, Pin.OUT)
button3LED = Pin(27, Pin.OUT)

button1State = 0

button1Released = 0

def disco():
    neoPixel.fill((random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255)))
    neoPixel.write()
    button1LED(random.randrange(0, 2))
    button2LED(random.randrange(0, 2))
    button3LED(random.randrange(0, 2))
    #time.sleep(0.1)

def discov2():
    for i in range(64):
        neoPixel[i] = (random.randrange(0, 255), random.randrange(0, 255), random.randrange(0, 255))
    neoPixel.write()
    #time.sleep(0.1)

def checkButton1():
    global button1State
    global button1Released

    button1StateOld = button1State
    button1State = button1.value()
    button1Released = button1StateOld == 1 and button1State == 0
    if button1Released:
        print("button1 was pressed")
        disco()

def countingUp():
    for i in range(63):
        neoPixel[i] = (255, 255, 255)
        neoPixel.write()
        time.sleep(1)

while True:
    countingUp()