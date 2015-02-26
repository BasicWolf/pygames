# The same game as in 201-203.
# The game logic and rendering is now decomposed into different functions

from random import randint

    
def main():
    game_state = GameState()
    
    while 1:
        render_new_game()
        game_loop(game_state)
        render_game_state(game_state)


class GameState:
    win_count = 0
    even_count = 0
    lost_count = 0
    total_games = 0
    result = ''

    round_ai_value = None
    round_pl_value = None
    

def render_new_game():
    print()
    print('------- New game -------')
    input('Roll the dice (press [Enter])')    

        
def game_loop(g):
    ai_value = randint(1, 6)
    pl_value = randint(1, 6)

    g.round_ai_value = ai_value
    g.round_pl_value = pl_value
    
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
    
def render_game_state(g):
    print('AI rolled %d' % g.round_ai_value)
    print('You rolled %d' % g.round_pl_value)
    
    print('Game is %s.' % g.result)

    print('Total games played: {}. Wins: {}, Even: {}, Losses: {}'.format(
        g.total_games, g.win_count, g.even_count, g.lost_count))


if __name__ == '__main__':
    main()
