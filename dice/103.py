# This is the same game as in 101.py.
# However, now you there is an AI (artificial intelligence) playing
# as well. 

from random import randint


win_count = 0
lost_count = 0

ai_win_count = 0
ai_lost_count = 0


def main():
    while 1:
        game_loop()

        
def game_loop():
    global win_count, lost_count, ai_win_count, ai_lost_count

    print()
    print('------- New game -------')

    dice_value = randint(1, 6)
    ai_picked_value = randint(1, 6)
    pl_picked_value = int(input('Pick a number from 1 to 6: '))

    if (pl_picked_value == dice_value):
        win_count += 1
        print('You won!')
    else:
        lost_count += 1
        print('You lost, the dice rolled: %d' % dice_value)

    if (ai_picked_value == dice_value):
        ai_win_count += 1
        print('AI won!')
    else:
        ai_lost_count += 1
        print('AI pickeded %d and lost' % ai_picked_value)

    print('You:      Wins: {}, Losses: {}'.format(win_count, lost_count))
    print('AI: Wins: {}, Losses: {}'.format(ai_win_count, ai_lost_count))


if __name__ == '__main__':
    main()
