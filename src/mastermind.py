import machine as m

## constant values
# game settings
PEGS_COUNT = 4
MAX_ATTEMPTS = 16

# GPIO settings
PIN_NEXT = 12
PIN_SELECT = 13


## mastermind code ( global variables )
# game variables
solution = []
board = [[] for i in range(MAX_ATTEMPTS)]
attempt = 0

# i/o variables
switches = {
    'next': m.Pin(PIN_NEXT, m.Pin.IN, m.Pin.PULL_DOWN),
    'select': m.Pin(PIN_SELECT, m.Pin.IN, m.Pin.PULL_DOWN),
}

## helper functions
def refresh_matrix():
    for row in range(attempt):
        pass

def check_victory():
    for i in range(PEGS_COUNT):
        if board[attempt][i] == solution[i]:
            break

# select start code
while len(solution) != PEGS_COUNT:
    if switches['next'].value():
        solution.append(color)
    elif switches['select'].value():
        # TODO: next color
        pass

    refresh_matrix()

# play 
while len(attempt) < MAX_ATTEMPTS or check_victory():
    while len(board[attempt]) < PEGS_COUNT:
        # TODO: get user input like on the start -> helper function ?
        pass
