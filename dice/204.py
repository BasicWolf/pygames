# simple dice game, me vs. friend random dice rolls
# same as 203, but with renderers in separate function

from random import randint


class GameState:
    win_count = 0
    even_count = 0
    lost_count = 0
    total_games = 0
    result = ''

    
def main():
    game_state = GameState()
    
    while 1:
        render_new_game()
        game_loop(game_state)
        render_game_state(game_state)


def render_new_game():
    print()
    print('------- New game -------')
    input('Roll the dice (press [Enter])')    

        
def game_loop(g):
    ai_value = randint(1, 6)
    pl_value = randint(1, 6)

    if (pl_value > ai_value):
        g.win_count += 1
        g.result = 'won'
    elif (pl_value == ai_value):
        g.even_count += 1
        g.result = 'even'
    elif (pl_value < ai_value):
        g.lost_count += 1
        g.result = 'lost'

    g.total_games += 1

    
def render_roll_results(ai_value, pl_value):
    print('AI rolled %d' % ai_value)
    print('You rolled %d' % pl_value)
    
    
def render_game_state(g):
    print('Game is %s.' % g.result)

    print('Total games played: {}. Wins: {}, Even: {}, Losses: {}'.format(
        g.total_games, g.win_count, g.even_count, g.lost_count))


if __name__ == '__main__':
    main()
