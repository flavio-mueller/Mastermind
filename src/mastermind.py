try:
    from neopixel import NeoPixel
    from machine import Pin
    import random
    import time
except:
    print("Imports are not available")

state_codeSetting = 0
state_autoSet = 1
state_codeGuessing = 2
state_autoGuess = 3
state_checking = 4
state_won = 5
state_outOfTries = 6
state_waitForReset = 7
state_reset = 8

state = state_reset

numPixel = 64
neoPin = Pin(18,Pin.OUT)

neoPixel = NeoPixel(neoPin, numPixel)

button1 = Pin(12, Pin.IN)
button2 = Pin(13, Pin.IN)
button3 = Pin(14, Pin.IN)
#button4 = Pin(15, Pin.IN)

button1LED = Pin(25, Pin.OUT)
button2LED = Pin(26, Pin.OUT)
button3LED = Pin(27, Pin.OUT)
#button4LED = Pin(28, Pin.OUT)

button1State = 0
button2State = 0
button3State = 0
#button4State = 0

button1Released = 0
button2Released = 0
button3Released = 0
#button4Released = 0

colBlue = (0, 0, 255)
colRed = (255, 0, 0)
colGreen = (0, 255, 0)
colYellow = (255, 255, 0)
colTurquoise = (0, 255, 255)
colPink = (255, 0, 255)

def checkButton1():
    global button1State
    global button1Released

    button1StateOld = button1State
    button1State = button1.value()
    button1Released = button1StateOld == 1 and button1State == 0
    if button1Released:
        print("button1 was pressed")

def checkButton2():
    global button2State
    global button2Released

    button2StateOld = button2State
    button2State = button2.value()
    button2Released = button2StateOld == 1 and button2State == 0
    if button2Released:
        print("button2 was pressed")

def checkButton3():
    global button3State
    global button3Released

    button3StateOld = button3State
    button3State = button3.value()
    button3Released = button3StateOld == 1 and button3State == 0
    if button3Released:
        print("button3 was pressed")

"""def checkButton4():
    global button4State
    global button4Released

    button4StateOld = button4State
    button4State = button4.value()
    button4Released = button4StateOld == 1 and button4State == 0
    if button4Released:
        print("button4 was pressed")
        state = state_reset
"""
def codeSetting():
    global state
    print(state)
    now = int(round(time.time()))
    print("Now: ", now)
    if now % 2 == 0:
        button1LED(1)
        neoPixel[1] = (255, 255, 255)
        neoPixel.write()
    else:
        neoPixel[1] = (255, 255, 255)
        neoPixel.write()
        button1LED(0)
    #state = state_codeGuessing

def autoSet():
    global state
    print(state)
    state = state_codeGuessing

def codeGuessing():
    global state
    print(state)
    state = state_checking

def autoGuess():
    global state
    print(state)
    state = state_checking

def checking():
    global state
    print(state)
    state = state_won

def won():
    global state
    print(state)
    state = state_waitForReset

def outOfTries():
    global state
    print(state)
    state = state_waitForReset

def waitForReset():
    global state
    print(state)
    state = state_reset

def reset():
    global state
    print(state)
    state = state_codeSetting
    print("Game was reseted")

while True:
    checkButton1()
    checkButton2()
    checkButton3()
    #checkButton4()

    if state == state_codeSetting:
        codeSetting()
    elif state == state_autoSet:
        autoSet()
    elif state == state_codeGuessing:
        codeGuessing()
    elif state == state_autoGuess:
        autoGuess()
    elif state == state_checking:
        checking()
    elif state == state_won:
        won()
    elif state == state_outOfTries:
        outOfTries()
    elif state == state_waitForReset:
        waitForReset()
    elif state == state_reset:
        reset()