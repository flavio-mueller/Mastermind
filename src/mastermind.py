from neopixel import NeoPixel
import machine as m
import time

## constant values
# game settings
MAX_ATTEMPTS = 16
PEGS_COUNT = 4

# hint pegs colors
PEGS_POS_RIGHT_COLOR = (  0,   0, 255), # blue
PEGS_POS_WRONG_COLOR = (255,   0,   0), # red

# hardware settings
NEOPIXEL_SIZE = 64
PIN_NEOPIXEL = 18

PIN_NEXT = 12
LED_NEXT = 25

PIN_SELECT = 13
LED_SELECT = 26

# PIN_THIRD = 
# LED_THIRD = 
# 
# PIN_FOURTH = 
# LED_FOURTH = 

# other constants
COLORS = [
    (  0,   0, 255), # blue
    (255,   0,   0), # red
    (  0, 255,   0), # green
    (255, 255,   0), # yellow
    (  0, 255, 255), # turquoise
    (255,   0, 255) # pink
]

## mastermind code ( global variables )
# game variables
solution = []
board = [[(0, 0, 0) for j in range(PEGS_COUNT)] for i in range(MAX_ATTEMPTS)]
attempt = 0

# i/o variables
display = NeoPixel(m.Pin(PIN_NEOPIXEL, m.Pin.OUT), NEOPIXEL_SIZE);
switches = {
    'next': m.Pin(PIN_NEXT, m.Pin.IN, m.Pin.PULL_DOWN),
    'select': m.Pin(PIN_SELECT, m.Pin.IN, m.Pin.PULL_DOWN),
}

leds = {
    'next': m.Pin(LED_NEXT, m.Pin.OUT, m.Pin.PULL_DOWN),
    'select': m.Pin(LED_SELECT, m.Pin.OUT, m.Pin.PULL_DOWN),
}

## helper functions
def refresh_matrix():
    for row in range(8):
        for col in range(8):
            if col >= len(board[row]):
                display[row*8 + col] = (0, 0, 0)
            else:
                display[row*8 + col] = board[row][col]

    display.write() 

# initialization


# select start code
color_index = 0
prev_time = time.time()
refresh_matrix()

while len(solution) <= PEGS_COUNT:
    if time.time() - prev_time < 1:
        continue
    else:
        prev_time = time.time()

    if switches['next'].value():
        print("codemaker: next")
        if len(solution): # clear the last led
            board[0][len(solution) -1] = (0, 0, 0)

        solution.append(COLORS[color_index])
        refresh_matrix()

    elif switches['select'].value():
        print("codemaker: select")
        color_index = 0 if color_index == len(COLORS)-1 else color_index +1
        board[0][len(solution)] = COLORS[color_index]
        refresh_matrix()


# play 
color_index = 0
prev_time = time.time()

while attempt < MAX_ATTEMPTS:
    # get user input
    while len(board[attempt]) < PEGS_COUNT:
        if time.time() - prev_time < 1:
            prev_time = time.time()
            continue

        if switches['next'].value():
            print("codebreaker: next")
            board[attempt].append(COLORS[color_index])
            refresh_matrix()
        elif switches['select'].values():
            print("codebreaker: select")
            color_index = 0 if color_index == len(COLORS)-1 else color_index +1
            refresh_matrix()

    # check victory
    if board[attempt] == solution:
        print("codebreaker won!")
        break

    # show hints
    for i in range(PEGS_COUNT):
        if board[attempt][i] == solution[i]:
            display[attempt*8 + i] = PEGS_POS_RIGHT_COLOR
            display.write()
        elif board[attempt][i] in solution:
            display[attempt*8 + i] = PEGS_POS_WRONG_COLOR
            display.write()
