# This is the same game as in 101.py.
# The difference is that the number of wins and losses is displayed
# after each round.

from random import randint


win_count = 0
lost_count = 0


def main():
    while 1:
        game_loop()

        
def game_loop():
    global win_count, lost_count
    
    print()
    print('------- New game -------')
    
    dice_value = randint(1, 6)
    picked_value = int(input('Pick a number from 1 to 6: '))

    if (picked_value == dice_value):
        win_count += 1
        print('You won!')
    else:
        lost_count += 1
        print('You lost, the dice rolled: %d' % dice_value)

    print('Wins: {}, Losses: {}'.format(win_count, lost_count))

    
if __name__ == '__main__':
    main()
