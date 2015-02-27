# This is an interesting dice game.
# The game is about collecting the number closest to 13.
# Any number of players can play the game.

# Rules:
# ======
#
# Before round
# ------------
#
# Players are rotated clockwise, so that the player who started
# the previous round, will be the last one to roll the dice in the
# following round.
#
# Round:
# ------
#
# 1.1 Player 1 rolls the dice and gets N points.
# 1.2 Player 2 rolls the dice and gets M points.
# 1.3 The process continues for all other players
# 2.1 The points collected at each roll are summed.
# 2.2 If a player's summary points exceed 13, he or she loses the round.
# 2.3 If a player's score is 13, he or she wins the round.
# 2.4 If a player's score is lower than 13, he or she can continue to the
#     next round, or skip the next round.
# 2.5 The round ends if all the remaining players decide skip the round. In
#     this case a player with highest summary points wins the game.
#     The game is considered a draw and 'no-win' for players if all the
#     summary points are equal.

def main():
    pass

class Game:        
    renderer = None
    state = None
    
    def __init__(self, renderer):
        self.renderer = renderer(self)

    def run(self):        
        while 1:
            self.loop()
        
    def loop(self):
        self.renderer.render_new_game()
        self.round()
        self.renderer.render_game_state()
        
        
class State:
    game = None
    
    def __init__(self, game):
        self.game = game

    def run(self):
        print('Not implemented')

        
class Round(GameState):
    pass

        
if __name__ == '__main__':
    main()
