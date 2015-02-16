# simple dice game, enter value - compare to rand(1, 6)

from random import randint


def main():
    while 1:
        game_loop()

def game_loop():
    print()
    print('------- New game -------')
    
    dice_value = randint(1, 6)
    guess_value = int(input('Enter the dice guess: '))

    if (guess_value == dice_value):
        print('You won!')
    else:
        print('You lost, the dice showed: %d' % dice_value)


if __name__ == '__main__':
    main()
