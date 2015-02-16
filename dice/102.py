# simple dice game, enter value - compare to rand(1, 6)
# shows wins/losses count

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
    guess_value = int(input('Enter the dice guess: '))

    if (guess_value == dice_value):
        win_count += 1
        print('You won!')
    else:
        lost_count += 1
        print('You lost, the dice showed: %d' % dice_value)

    print('Wins: {}, Losses: {}'.format(win_count, lost_count))

    
if __name__ == '__main__':
    main()
