try:
    from neopixel import NeoPixel
    from machine import Pin
    import pyb
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
maxRows = 8
neoPin = Pin(18, Pin.OUT)

neoPixel = NeoPixel(neoPin, numPixel)

button1 = Pin(12, Pin.IN)
button2 = Pin(13, Pin.IN)
button3 = Pin(14, Pin.IN)
# button4 = Pin(15, Pin.IN)

button1LED = Pin(25, Pin.OUT)
button2LED = Pin(26, Pin.OUT)
button3LED = Pin(27, Pin.OUT)
# button4LED = Pin(28, Pin.OUT)

button1State = 0
button2State = 0
button3State = 0
# button4State = 0

button1Released = 0
button2Released = 0
button3Released = 0
# button4Released = 0

brightness = 10

colBlue = (0, 0, brightness)
colRed = (brightness, 0, 0)
colGreen = (0, brightness, 0)
colYellow = (brightness, brightness, 0)
colTurquoise = (0, brightness, brightness)
colPink = (brightness, 0, brightness)
colBlack = (0, 0, 0,)
colWhite = (brightness, brightness, brightness)

colors = [colBlue, colRed, colGreen, colYellow, colTurquoise, colPink, colBlack, colWhite]

curCol = 0

colorSet = [0, 0, 0, 0]
rowColorSet = [[0 for x in range(6)] for y in range(maxRows)]

temBoolean = 1

row = 1

counter = 0


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
    global button3State, state, button3Released
    button3StateOld = button3State
    button3State = button3.value()
    button3Released = button3StateOld == 1 and button3State == 0
    if button3Released:
        print("button3 was pressed")
        state = state_reset


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
    global state, curCol, colorSet, counter
    button2LED(1)
    timer = pyb.Timer(0)
    timer.init(freq=4)
    timer.callback(lambda t: pyb.button1LED(1).toggle())
    if counter == 4:
        print("Colors were set")
        counter = 0
        curCol = 0
        timer.callback(None)
        button1LED(0)
        button2LED(0)
        state = state_codeGuessing
    if button1Released:
        curCol = (curCol + 1) % 6
        neoPixel[counter] = (colors[curCol])
        neoPixel.write()
        print("Next Color")

    if button2Released:
        print("Color set")
        colorSet[counter] = curCol
        curCol = 0
        counter += 1
        if counter < 4:
            neoPixel[counter] = (colors[curCol])
            neoPixel.write()


def autoSet():
    global state
    print(state)
    state = state_codeGuessing


def codeGuessing():
    global state, curCol, counter, row, temBoolean, rowColorSet
    button2LED(1)
    timer1 = pyb.Timer(1)
    timer1.init(freq=4)
    timer1.callback(lambda t: pyb.button1LED(1).toggle())
    if temBoolean:
        neoPixel[counter + 8 * row] = (colors[curCol])
        neoPixel.write()
        temBoolean = 0

    if button1Released:
        curCol = (curCol + 1) % 6
        neoPixel[counter + 8 * row] = (colors[curCol])
        neoPixel.write()
        print("Next Color")

    if button2Released:
        print("Color set")
        print(row, counter)
        rowColorSet[row][counter] = curCol
        curCol = 0
        counter += 1
        if counter < 4:
            neoPixel[counter + 8 * row] = (colors[curCol])
            neoPixel.write()

    if counter == 4:
        print("Colors were set")
        counter = 0
        curCol = 0
        temBoolean = 1
        timer1.callback(None)
        button1LED(0)
        button2LED(0)
        state = state_checking


def autoGuess():
    global state
    print(state)
    state = state_checking


def checking():
    global state, row, rowColorSet
    global colorSet
    print("State: Checking")
    counterGreen = 0
    counterWhite = 0
    tempColorSet = list(colorSet)
    tempRowColorSet = list(rowColorSet)
    for i in range(4):
        if tempColorSet[i] == tempRowColorSet[row][i]:
            neoPixel[4 + counterGreen + 8 * row] = colGreen
            tempRowColorSet[row][i] = -1
            tempColorSet[i] = -2
            counterGreen += 1
            neoPixel.write()

    for i in range(4):
        for j in range(4):
            if tempColorSet[i] == tempRowColorSet[row][j]:
                neoPixel[4 + counterGreen + counterWhite + 8 * row] = colWhite
                neoPixel.write()
                counterWhite += 1
                tempRowColorSet[row][j] = -3
                tempColorSet[i] = -4

    tempRowColorSet[row][4] = counterGreen
    tempRowColorSet[row][5] = counterWhite

    rowColorSet[row][4] = counterGreen
    rowColorSet[row][5] = counterWhite

    if counterGreen == 4:
        state = state_won
    elif row < (maxRows - 1):
        row += 1
        state = state_codeGuessing
    else:
        state = state_outOfTries

    print("Colorset: ", colorSet)
    print("Rowcolorset: ", rowColorSet)
    print("temprowcolorset: ", tempRowColorSet)


def won():
    global state
    print("You have won")
    neoPixel.fill(colGreen)
    neoPixel.write()
    state = state_waitForReset


def outOfTries():
    global state
    print("No tries left")
    neoPixel.fill(colRed)
    neoPixel.write()
    state = state_waitForReset


def waitForReset():
    global state
    print("Waiting for Reset (Button 3)")


def reset():
    global state, counter
    for i in range(numPixel):
        neoPixel[i] = colWhite
        neoPixel.write()
        time.sleep(0.01)
    neoPixel.fill(colBlack)
    counter = 0
    neoPixel[counter] = (colors[curCol])
    neoPixel.write()
    state = state_codeSetting
    print("Game was reseted")


while True:
    checkButton1()
    checkButton2()
    checkButton3()
    # checkButton4()

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
