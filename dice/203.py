# The same game as in 201 and 202.
# The state of the game is now stored in a class. 

from random import randint


def main():
    game_state = GameState()
    
    while 1:
        game_loop(game_state)


class GameState:
    win_count = 0
    even_count = 0
    lost_count = 0
    total_games = 0

        
def game_loop(g):
    print()
    print('------- New game -------')
    
    input('Roll the dice (press [Enter])')

    ai_value = randint(1, 6)
    pl_value = randint(1, 6)

    print('AI rolled %d' % ai_value)
    print('You rolled %d' % pl_value)

    if (pl_value > ai_value):
        g.win_count += 1
        print('You won!')
    elif (pl_value == ai_value):
        g.even_count += 1
        print('Even')
    elif (pl_value < ai_value):
        g.lost_count += 1
        print('You lost')

    g.total_games += 1
    
    print('Total games played: {}. Wins: {}, Even: {}, Losses: {}'.format(
        g.total_games, g.win_count, g.even_count, g.lost_count))


if __name__ == '__main__':
    main()
