import random


# Random mode, when you make a move the opponent chooses a random move from the valid moves and makes that move
# Performance: pretty bad
def RandomBot(moves):

    return random.randint(0, len(moves) - 1)

