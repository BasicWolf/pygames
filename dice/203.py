# simple dice game, me vs. friend random dice rolls
# same as 202, but with game state in dictionary

from random import randint

def main():
    game_state = {
        'game_result': '',
        'win_count': 0,
        'even_count': 0,
        'lost_count': 0,
        'total_games': 0,
    }

    while 1:
        render_new_game()
        game_loop(game_state)
        render_game_state(game_state)

def game_loop(g):
    input('Roll the dice (press [Enter])')

    ai_value = randint(1, 6)
    pl_value = randint(1, 6)

    print('AI rolled %d' % ai_value)
    print('You rolled %d' % pl_value)

    if (pl_value > ai_value):
        g['win_count'] += 1
        g['game_result'] = 'won'
    elif (pl_value == ai_value):
        g['even_count'] += 1
        g['game_result'] = 'even'
    elif (pl_value < ai_value):
        g['lost_count'] += 1
        g['game_result'] = 'lost'

    g['total_games'] += 1

def render_new_game():
    print()
    print('------- New game -------')

def render_game_state(g):
    print('Game is %s.' % g['game_result'])

    print('Total games played: {}. Wins: {}, Even: {}, Losses: {}'.format(
        g['total_games'], g['win_count'], g['even_count'], g['lost_count']))


if __name__ == '__main__':
    main()
