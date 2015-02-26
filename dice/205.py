# The same game as in 201-204.
# The game (game state) and renderer are now separate classes

from random import randint

        
def main():    
    game = Game(ConsoleRenderer)
    game.run()
    

class Game:
    win_count = 0
    even_count = 0
    lost_count = 0
    total_games = 0
    result = ''

    round_ai_value = None
    round_pl_value = None
    
    renderer = None
    
    def __init__(self, renderer):
        self.renderer = renderer(self)

    def run(self):        
        while 1:
            self.loop()
        
    def loop(self):
        self.renderer.render_new_game()
        self.round()
        self.renderer.render_game_state()
        
    def round(self):        
        ai_value = randint(1, 6)
        pl_value = randint(1, 6)

        self.round_ai_value = ai_value
        self.round_pl_value = pl_value
        
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


class ConsoleRenderer:
    game = None
    
    def __init__(self, game):
        self.game = game
        
    def render_new_game(self):
        print()
        print('------- New game -------')
        input('Roll the dice (press [Enter])')    

    def render_game_state(self):
        g = self.game

        print('AI rolled %d' % g.round_ai_value)
        print('You rolled %d' % g.round_pl_value)

        print('Game is %s.' % g.result)

        print('Total games played: {}. Wins: {}, Even: {}, Losses: {}'.format(
            g.total_games, g.win_count, g.even_count, g.lost_count))

        
if __name__ == '__main__':
    main()
