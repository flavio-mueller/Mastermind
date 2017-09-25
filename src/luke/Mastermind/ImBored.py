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

xCoordiante = 4
yCoordinate = 2
yForce = 0
jumped = False
jumpInput = False

mapp = [[1, 1, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 0, 0, 5, 0],
       [1, 0, 0, 0, 0, 0, 0, 0],
       [1, 0, 0, 0, 1, 0, 0, 0],
       [1, 0, 0, 0, 1, 0, 0, 0],
       [1, 0, 0, 0, 1, 0, 0, 0],
       [0, 0, 0, 0, 0, 0, 0, 0],
       [1, 1, 0, 0, 0, 0, 0, 0]]

#def SetLedToColor(x,y,color):
#    neoPixel[x+y*8] = color
#   neoPixel.write()


def ApplyMovement(x):
    global mapp, xCoordiante,yCoordinate
    newX = (xCoordiante+x) % 8
    if(mapp[newX][yCoordinate] != 0):
        if(x > 0):
            ApplyMovement(x-1)
            return
        if(x < 0):
            ApplyMovement(x+1)
            return


    xCoordiante = newX;


def Draw():
    global colors,mapp, xCoordiante,yCoordinate
    for x in range(0,8):
        for y in range(0,8):
            if(mapp[x][y]!= 5):
                neoPixel[8+x + y * 8] = colors[mapp[x][y]]
            if(mapp[x][y]== 5):
                neoPixel[8+x + y * 8] = (random.randrange(0,255),random.randrange(0,255),random.randrange(0,255))


    neoPixel[8+xCoordiante+ 8*yCoordinate] = colors[2]
    neoPixel.write()

def Update():
    global mapp, jumpInput
    move = 0
    if(button0.value() == 1):
       move += 1
    if(button1.value() == 1):
        move -= 1
    if(jumpInput == True):
        Jump()
        jumpInput = False

    ApplyMovement(move)
    ApplyForce()
    Draw()
    #print(mapp)
    #print("x: ", xCoordiante, "y: ", yCoordinate)

def ApplyForce():
    global xCoordiante,yCoordinate,yForce,mapp,jumped
    if(mapp[xCoordiante][(yCoordinate+1)%8] == 0):
        yForce -= 1
    if(mapp[xCoordiante][(yCoordinate+1)%8] == 1):
        if(jumped == False):
            yForce = 0
        else:
            jumped = False

    for x in range(0,abs(yForce)):
        if(yForce > 0):
            if(mapp[xCoordiante][(yCoordinate+1)%8] == 0):
                yCoordinate=  (yCoordinate+1)%8
        if(yForce < 0):
            if(mapp[xCoordiante][(yCoordinate-1)%8] == 0):
                yCoordinate = (yCoordinate - 1) % 8

    if(yForce < -4):
        yForce = -4

def Jump():
    global mapp,xCoordiante, yCoordinate,yForce,jumped
    if (mapp[xCoordiante][(yCoordinate + 1) % 8] == 1):
        yForce = -2
        jumped = True

def MainLoop():
    neoPixel.timing = 1
    global startTime,lastFrameTime,deltatime,frameRate, jumpInput
    while(True):
        if(button2.value == 1):
            jumpInput = True
        if(time.time()-(1/frameRate) > lastFrameTime):
            deltatime = time.time()-lastFrameTime
            lastFrameTime = time.time()
            Update()

MainLoop()