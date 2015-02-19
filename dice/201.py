# This is a simple dice game.
# The rules are following:
# 1. A human player (you) rolls a virtual dice.
# 2. An AI opponent rolls a virtual dice.
# 3. The winner is the player (either human or AI) with the biggest rolled score.
# 4. If the scores are equal the round is counted as 'even'.

from random import randint


win_count = 0
even_count = 0
lost_count = 0
total_games = 0


def main():
    while 1:
        game_loop()

        
def game_loop():
    global win_count, lost_count, even_count, total_games

    print()
    print('------- New game -------')
    input('Roll the dice (press [Enter])')
    
    ai_value = randint(1, 6)
    pl_value = randint(1, 6)

    print('AI rolled %d' % ai_value)
    print('You rolled %d' % pl_value)
    
    if (pl_value > ai_value):
        win_count += 1
        print('You won!')
    elif (pl_value == ai_value):
        even_count += 1
        print('Even')
    elif (pl_value < ai_value):
        lost_count += 1
        print('You lost')

    total_games += 1
    
    print('Total games played: {}. Wins: {}, Even: {}, Losses: {}'.format(
        total_games, win_count, even_count, lost_count))


if __name__ == '__main__':
    main()
