# dice game, get value closest to 13 or loose

from random import randint

game = {
    'win_count' : 0,
    'even_count' : 0,
    'lost_count': 0,
    
}
win_count = 0
even_count = 0
lost_count = 0
total_games = 0
me_counter = 0
ai_counter = 0
ai_stop = False
me_stop = False

def main():
    while 1:
        game_loop()

def game_loop():
    print()
    print('------- New game -------')

    game_in_progress = False
    while game_in_progress:
        game_in_progress = round_loop()
        
def round_loop():
    global win_count, lost_count, even_count, total_games    
    global ai_stop, me_stop, ai_counter, me_counter

    print()
    print('---- Next round ----')

    if not me_stop:
        my_input = input('Roll the dice (press [Enter]) or write "stop" to stop rolling')
        if my_input == 'stop':
            me_stop = True
            
    if not me_stop:
        my_value = randint(1, 6)
        print('You rolled %d' % my_value)
    else:
        my_value = 0
        print('You stopped rolling')

    ai_stop = should_ai_stop()
    if not ai_stop:
        ai_value = randint(1, 6)
        print('AI rolled %d' % ai_value)        
    else:
        ai_value = 0
        print('AI stopped rolling')

    me_counter += my_value
    ai_counter += ai_value
    
    if me_stop and ai_stop:
        win_count += 1
        print('You won!')
    elif my_value == ai_value:
        even_count += 1
        print('Even')
    elif my_value < ai_value:
        lost_count += 1
        print('You lost')

    total_games += 1
    
    print('Total games played: {}. Wins: {}, Even: {}, Losses: {}'.format(total_games, win_count, even_count, lost_count))

    
def should_ai_stop(ai_counter, me_counter, me_stop):
    if ai_counter == 13:
        return True
    elif ai_counter <= me_counter <= 12 and not me_stop:
        return False
    if me_counter <= 13 and n
    return value >= 11
    

if __name__ == '__main__':
    main()
