
## constant values
# game settings
MAX_ATTEMPTS = 16
PEGS_COUNT = 4

# hint pegs colors
PEGS_POS_RIGHT_COLOR = "red"
PEGS_POS_WRONG_COLOR = "blue"

COLORS = {
    "blue": "blue",
    "red": "red",
    "green":"green",
    "yellow": "yellow",
    "turquoise": "turquoise",
    "pink": "pink"
}

## mastermind code ( global variables )
# game variables
solution = []
board = [[] for i in range(MAX_ATTEMPTS)]
attempt = 0

## helper functions
def check_victory():
    if board[attempt] == solution:
        return True

    hints = []
    for i in range(PEGS_COUNT):
        if board[attempt][i] == solution[i]:
            hints.append(COLORS[PEGS_POS_RIGHT_COLOR])
        elif solution[i] in board[attempt]:
            hints.append(COLORS[PEGS_POS_WRONG_COLOR])

    return hints

# select start code
print("colors: " + str(COLORS))
solution = input("enter your " + str(PEGS_COUNT) + " pegs code separated by spaces: ").split()

# play 
while attempt < MAX_ATTEMPTS:
    peg = 0
    while len(board[attempt]) < PEGS_COUNT:
        board[attempt].append(COLORS[input("your peg: ")])

    victory = check_victory()
    
    if victory == True:
        print("You won")
        break
    else:
        print("hints: " + str(victory))
        attempt += 1
