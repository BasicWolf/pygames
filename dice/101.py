# This is a very simple dice game.
# The rules are following:
# 1. A human player (you) picks a number from 1 to 6.
# 2. The computer rolls a virtual dice.
# 3. You win, if the number you picked is correct, otherwise you loose.

from random import randint


def main():
    while 1:
        game_loop()

        
def game_loop():
    print()
    print('------- New game -------')
    
    dice_value = randint(1, 6)
    picked_value = int(input('Pick a number from 1 to 6: '))

    if (picked_value == dice_value):
        print('You won!')
    else:
        print('You lost, the dice rolled: %d' % dice_value)


if __name__ == '__main__':
    main()
