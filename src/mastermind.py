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
board = [[] for i in range(MAX_ATTEMPTS)]
attempt = 0

# i/o variables
ctrl_switches = {
    'next': m.Pin(PIN_NEXT, m.Pin.IN, m.Pin.PULL_DOWN),
    'select': m.Pin(PIN_SELECT, m.Pin.IN, m.Pin.PULL_DOWN),
    '3': None,
    '4': None
}

## helper functions
def 

# select start code

# play 

