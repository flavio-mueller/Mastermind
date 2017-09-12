try:
    from neopixel import NeoPixel
    from machine import Pin
    import random
    import time
except:
    print("Imports are not available")


#neopixel

numPixel = 64
neoPin = Pin(18,Pin.OUT)
neoPixel = NeoPixel(neoPin, numPixel)

# global variables

state = [0,0,0]
oldState = [0,0,0]
solution = [0,0,0,0]
pointerIndex = 0
colors = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(255,0,127)]

#buttons
button0 = Pin(12, Pin.IN)
button1 = Pin(13, Pin.IN)
button2 = Pin(14, Pin.IN)



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

# Waits for input and returns next input
def WaitForNextButtonInput():
    while(True):
        UpdateButtons()
        test = CheckButtons()
        if(test != -1):
            return test


# let's the user choose the startcode
def SetStartcode():
    global solution, pointerIndex
    while(True):
        SetSolutionLEDRow()
        SetCursorLed()
        print("tick")
        test = WaitForNextButtonInput()
        if(test == 2 or pointerIndex == 3):
            StartAlgorithm()
            break
        if(test == 1):
            solution[pointerIndex] = (solution[pointerIndex]+1)%6

        if(test == 0):
            pointerIndex = (pointerIndex+1)%4

# starts the algorithm that plays the game
def StartAlgorithm():
    ClearPannel()
    print("Finished!")

#function which sets the top line of the LED pannel to the solution array
def SetSolutionLEDRow():
    global solution,colors
    for x in range(0,4):
        neoPixel[x] = colors[solution[x]]
        neoPixel.write()

# clears a row of LEDs
def DeleteRow(row):
    for x in range(0,8):
        neoPixel[x+(8*row)] = (0,0,0)
    neoPixel.write()

# clears the entire pannel
def ClearPannel():
    neoPixel.fill((0,0,0))
    neoPixel.write()


# sets the cursor LED when chosing the start colors
def SetCursorLed():
    global pointerIndex

    DeleteRow(1)
    neoPixel[pointerIndex+8] = (0, 255, 0)
    neoPixel.write()



neoPixel[42] = (0,255,0)
neoPixel.write()
print("worked")

SetStartcode()

