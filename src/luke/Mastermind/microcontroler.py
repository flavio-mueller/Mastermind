try:
    from neopixel import NeoPixel
    from machine import Pin
    import random
    import time
    import  gc
except:
    print("Imports are not available")


#neopixel

numPixel = 64+64+8
neoPin = Pin(18,Pin.OUT)
neoPixel = NeoPixel(neoPin, numPixel)

# global variables

state = [0,0,0,0]
oldState = [0,0,0,0]
solution = [0,0,0,0]
pointerIndex = 0
colors = [(255,0,0),(0,255,0),(0,0,255),(255,255,0),(0,255,255),(255,0,127)]
tries = 0
arrayOfAllStillPossibleCombinations = [[]]

#buttons
button0 = Pin(12, Pin.IN)
button1 = Pin(13, Pin.IN)
button2 = Pin(14, Pin.IN)#not working
button3 = Pin(17, Pin.IN)


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
    neoPixel.timing = 1
    global solution, pointerIndex
    while(True):
        SetSolutionLEDRow()
        SetCursorLed()
        test = WaitForNextButtonInput()


        if(test == 3):
            StartAlgorithm()
            break
        if(test == 1):
            solution[pointerIndex] = (solution[pointerIndex]+1)%6

        if(test == 0):
            pointerIndex = (pointerIndex+1)%4

# starts the algorithm that plays the game
def StartAlgorithm():
    global  solution, arrayOfAllStillPossibleCombinations
    DeleteRow(1)
    arrayOfAllStillPossibleCombinations = GetAllCombinationsArray()
    gc.collect()
    SolveMastermind(solution)

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

# compares to colorcode arrays and returns a touple with the correct and the semi correct values.
def compare(a, b):
    a = list(a)
    b = list(b)

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

# returns all arrays that could also have the same solution as the result from arr
#by compare()ing arr and all possible combinations
def GetSimilarArrays(index, result):
    global arrayOfAllStillPossibleCombinations

    k = list(arrayOfAllStillPossibleCombinations[index])
    del (arrayOfAllStillPossibleCombinations[index])
    x = 0
    while (x < len(arrayOfAllStillPossibleCombinations)):

        sol = compare(arrayOfAllStillPossibleCombinations[x], k)

        if (sol != result):
            del (arrayOfAllStillPossibleCombinations[x])
            x -= 1
        x += 1

#returns an array with all possible combinations
def GetAllCombinationsArray():
    arr = [[None for _ in range(4)] for _ in range(1296)]
    i = 0

    for x in range(0, 6):
        for y in range(0, 6):
            for z in range(0, 6):
                for j in range(0, 6):
                    arr[i][0] = x
                    arr[i][1] = y
                    arr[i][2] = z
                    arr[i][3] = j
                    i += 1
    return arr


#function that solves the mastermind and displays it
def SolveMastermind(solution):
    global tries,arrayOfAllStillPossibleCombinations

    index = ((len(arrayOfAllStillPossibleCombinations)*4) // 13)


    copiedArray = list(arrayOfAllStillPossibleCombinations[index])

    touple = compare(copiedArray,solution)

    #output the try and result on the display
    WriteIterationToLEDs(index,touple)

    GetSimilarArrays(index, touple)
    gc.collect()



    if( len(arrayOfAllStillPossibleCombinations)== 0):
       # output a fancy solved line
        return
    tries += 1
    SolveMastermind(solution)


def WriteIterationToLEDs(index, result):
    global arrayOfAllStillPossibleCombinations
    row = tries+2

    for x in range (0,4):
        neoPixel[x+(row*8)] = colors[arrayOfAllStillPossibleCombinations[index][x]]

    total = result[0]+result[1]
    for x in range(0,result[0]):
        neoPixel[x+8-total+(row*8)] = (255,255,255)
    for x in range(0,result[1]):
        neoPixel[x+8-total+(row*8)] = (255,0,0)



    neoPixel.write()


SetStartcode()

