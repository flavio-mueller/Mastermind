try:
    from neopixel import NeoPixel
    from machine import Pin
    import random
    import time
    import  gc
except:
    print("Imports are not available")



numPixel = 128+8
neoPin = Pin(18,Pin.OUT)
neoPixel = NeoPixel(neoPin, numPixel)

#buttons
button0 = Pin(12, Pin.IN)
button1 = Pin(13, Pin.IN)
button2 = Pin(14, Pin.IN)
button3 = Pin(15, Pin.IN)

state = [0,0,0,0]
oldState = [0,0,0,0]



# returns the id of the pressed button or -1 if no button was pressed.
def CheckButtons():
    global state
    if(oldState[0] == 1 and state[0] == 0):
        return 0
    if(oldState[1] == 1 and state[1] == 0):
        return 1
    if(oldState[2] == 1 and state[2] == 0):
        return 2
    if(oldState[3] == 1 and state[3] == 0):
        return 3

    return -1



#Updates the buttonstates
def UpdateButtons():
    global state
    oldState[0] = state[0]
    oldState[1] = state[1]
    oldState[2] = state[2]
    oldState[3] = state[3]


    state[0] = button0.value()
    state[1] = button1.value()
    state[2] = button2.value()
    state[3] = button3.value()

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
        test = WaitForNextButtonInput()
        if (test == 3):
            neoPixel[21] = (0, 255, 127)
            neoPixel.write()

        if(test == 2):
            neoPixel[21] = (255,0,0)
            neoPixel.write()

        if(test == 1):
            neoPixel[21] = (0, 255, 0)
            neoPixel.write()

        if(test == 0):
            neoPixel[21] = (0, 255, 127)
            neoPixel.write()


for x in range(0,17,1):
        neoPixel[(x%8)  + (x * 8)] = (255, 255, 255)

neoPixel.write()
SetStartcode()