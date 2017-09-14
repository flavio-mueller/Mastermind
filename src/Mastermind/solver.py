try:
    from neopixel import NeoPixel
    from machine import Pin
    import random
    import time
    import math
    import  gc
except:
    print("Imports are not available")


#neopixel

numPixel = 64
neoPin = Pin(18,Pin.OUT)
neoPixel = NeoPixel(neoPin, numPixel)
neoPixel.timing = 1

# global variables
COLORS = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(255,0,127)]

state = [0,0,0]
oldState = [0,0,0]
pointerIndex = 0

#buttons
button0 = Pin(12, Pin.IN)
button1 = Pin(13, Pin.IN)
button2 = Pin(17, Pin.IN)


# returns the id of the pressed button or -1 if no button was pressed.
def CheckButtons():
    global state
    if(oldState[0] == 1 and state[0] == 0):
        return 0
    if(oldState[1] == 1 and state[1] == 0):
        return 1
    if(oldState[2] == 1 and state[2] == 0):
        return 2

    return -1

#Updates the buttonstates
def UpdateButtons():
    global state
    oldState[0] = state[0]
    oldState[1] = state[1]
    oldState[2] = state[2]


    state[0] = button0.value()
    state[1] = button1.value()
    state[2] = button2.value()

#function which sets the top line of the LED pannel to the solution array
def SetSolutionLEDRow():
    global solution,COLORS

# clears a row of LEDs
def ClearRow(row):
    for x in range(0,8):
        neoPixel[x+(8*row)] = (0,0,0)
    neoPixel.write()

# clears the entire pannel
def ClearPannel():
    neoPixel.fill((0,0,0))
    neoPixel.write()

# sets the cursor LED when chosing the start COLORS
def SetCursorLed():
    global pointerIndex


def WriteIterationToLEDs(index, result):
    global combinations
    row = tries+2

    for x in range (0,4):
        neoPixel[x+(row*8)] = COLORS[combinations[index][x]]

    total = result[0]+result[1]
    for x in range(0,result[0]):
        neoPixel[x+8-total+(row*8)] = (255,255,255)
    for x in range(0,result[1]):
        neoPixel[x+8-total+(row*8)] = (255,0,0)
    neoPixel.write()

# compares to colorcode arrays and returns a touple with the correct and the semi correct values.
def compare(a, b):
    a = bytearray(a)
    b = bytearray(b)

    corrects = 0;
    semiCorrects = 0;


    for x in range(0,4):
        if (a[x] == b[x]):
            a[x] = -1
            b[x] = -2
            corrects += 1

    for x in range(0,4):
        for y in range(0,4):
            if(a[x] == b[y]):
                a[x] = -1
                b[y] = -2
                semiCorrects += 1
                break

    return(corrects,semiCorrects)

## let's the user choose the startcode
solution = [0,0,0,0]
while(True):

    # SetSolutionLedRow()
    for x in range(0,4):
        neoPixel[x] = COLORS[solution[x]]
        neoPixel.write()

    # SetCursorLed()
    ClearRow(1)
    neoPixel[pointerIndex+8] = (0, 255, 0)
    neoPixel.write()

    # test = WaitForNextButtonInput()
    while True:
        UpdateButtons()
        test = CheckButtons()
        if(test != -1):
            break

    if(test == 0):
        pointerIndex = (pointerIndex+1)%4
    elif(test == 1):
        solution[pointerIndex] = (solution[pointerIndex]+1)%6
    elif(test == 2 or pointerIndex == 3):
        break

ClearRow(1)

## starts the algorithm that plays the game
gc.collect()
# get all combinations
combinations = []

for x in range(0, 6):
    for y in range(0, 6):
        for z in range(0, 6):
            for j in range(0, 6):
                combinations.append([x, y, z, j])

print("free:  " + str(gc.mem_alloc()))
print("alloc: " + str(gc.mem_free()))

# solve mastermind
tries = 0
while len(combinations) != 0:
    index = int(math.sqrt(len(combinations)) -1) # random starting point
    result = compare(list(combinations[index]), solution)

    WriteIterationToLEDs(index,result)

    # returns all arrays that could also have the same solution as the result
    # from arr by compare()ing arr and all possible combinations
    k = list(combinations[index])
    del (combinations[index])

    x = 0
    while (x < len(combinations)):
        if (compare(combinations[x], k) != result):
            del combinations[x]
            x -= 1
        x += 1
        
    gc.collect()
    tries += 1
