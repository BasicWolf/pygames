# simple dice game, me vs. friend random dice rolls
# same as 203, but with renderers in separate function

from random import randint


class Game:
    win_count = 0
    even_count = 0
    lost_count = 0
    total_games = 0
    result = ''
    renderer = None
    
    def __init__(self, renderer):
        self.renderer = renderer

    def run(self):        
        while 1:
            self.loop()
        
    def loop(self):
        self.renderer.new_game()
        
    def round(self):        
        ai_value = randint(1, 6)
        pl_value = randint(1, 6)

        if (pl_value > ai_value):
            self.win_count += 1
            self.result = 'won'
        elif (pl_value == ai_value):
            self.even_count += 1
            self.result = 'even'
        elif (pl_value < ai_value):
            self.lost_count += 1
            self.result = 'lost'

        self.total_games += 1


class BeautifulConsoleRenderer:
    game = None
    def __init__(self, game):
        self.game = game
        
    def new_game(self):
        print()
        print('------- New game -------')
        input('Roll the dice (press [Enter])')    

    def roll_results(ai_value, pl_value):
        print('AI rolled %d' % self.value_to_symbol(ai_value))
        print('You rolled %d' % self.value_to_symbol(pl_value))
        
    def render_game_state(self):
        g = self.game
        print('Game is %s.' % g.result)

        print('Total games played: {}. Wins: {}, Even: {}, Losses: {}'.format(
            g.total_games, g.win_count, g.even_count, g.lost_count))

    def value_to_symbol(self, value):
        chars = '⚀⚁⚂⚃⚄⚅'
        return chars[value - 1]
        

class ConsoleRenderer:
    game = None
    def __init__(self, game):
        self.game = game
        
    def new_game(self):
        print()
        print('------- New game -------')
        input('Roll the dice (press [Enter])')    

    def roll_results(ai_value, pl_value):
        print('AI rolled %d' % ai_value)
        print('You rolled %d' % pl_value)
    
    
    def render_game_state(self):
        g = self.game
        print('Game is %s.' % result)

        print('Total games played: {}. Wins: {}, Even: {}, Losses: {}'.format(
            g.total_games, g.win_count, g.even_count, g.lost_count))
        
    
def main():
    renderer = ConsoleRenderer()
    game = Game(renderer)
    game.run()
    


if __name__ == '__main__':
    main()
