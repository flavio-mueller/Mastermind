try:
    from neopixel import NeoPixel
    from machine import Pin
    import random
    import time
except:
    print("Imports are not available")

#neopixel

numPixel = 64+64+8
neoPin = Pin(18,Pin.OUT)
neoPixel = NeoPixel(neoPin, numPixel)

#constants
green = (0,40,0)
white = (5,5,5)
red = (40,0,0)
brown = (204,102,0)

#buttons
button0 = Pin(12, Pin.IN)
button1 = Pin(13, Pin.IN)
button2 = Pin(17, Pin.IN)

colors = (white,green,red,brown)

#global variables
startTime = time.time()
lastFrameTime = time.time()
deltatime = 0
frameRate = 4

yForce = 0
jumped = False
jumpInput = False

xCoordinate = 3
yCoordinate = 1

def Update():
    global  jumpInput

    if(jumpInput == True):
        Jump()
        jumpInput = False
    elif(yCoordinate > 1):
        yCoordinate -= 1


def Jump():
    global xCoordinate,yCoordinate, jumped
    if (yCoordinate == 1):
        yCoordinate += 3
        jumped = True

def MainLoop():
    global startTime,lastFrameTime,deltatime,frameRate, jumpInput, xCoordinate,yCoordinate
    neoPixel.timing = 1

    while(True):
        if(button0.value == 1):
            jumpInput = True
        if(time.time()-(1/frameRate) > lastFrameTime):
            deltatime = time.time()-lastFrameTime
            lastFrameTime = time.time()
            Update()

def Draw():
    global xCoordinate,yCoordinate
    numPixel.fill((0,0,0))
    numPixel[8+xCoordinate+yCoordinate*8] = (255,0,0)

MainLoop()