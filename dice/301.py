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
#     next round, or skip all the next rounds.
# 2.5 The round ends if all the remaining players decide to skip the round. In
#     this case a player with highest summary points wins the game.
#     The game is considered a draw and 'no-win' for players if all the
#     summary points are equal.

from abc import ABCMeta, abstractmethod
from random import randint

from getch import getch


def main():
    game = Game()
    game.run()


class Game:
    def __init__(self):
        self.renderer = ConsoleRenderer(self)
        self.state = MainMenuState(self)
        self.status = GameStatus()
        
    def run(self):
        while 1:
            next_state = self.state.run()
            self.state = next_state

    

class GameState(metaclass=ABCMeta):
    def __init__(self, game):
        self.game = game
        self.renderer = game.renderer.get_state_renderer(self)

    @abstractmethod
    def run(self):
        pass


class MainMenuState(GameState):
    ACTION_UNKNOWN = 0
    ACTION_START_GAME = 1
    ACTION_EXIT = 2

    def run(self):
        action = self.ACTION_UNKNOWN;

        while(action == self.ACTION_UNKNOWN):
            self.renderer.show_main_menu()
            action = self.renderer.read_main_menu_input()
            return self.get_next_state(action)
        
    def get_next_state(self, action):
        transitions = {
            self.ACTION_START_GAME: NewGameState,
            self.ACTION_EXIT: ExitState
        }
        next_state_class = transitions[action]
        next_state_obj = next_state_class(self.game)
        return next_state_obj        


class NewGameState(GameState):
    def run(self):
        status = GameStatus()
        return NewRoundState(self.game, self.status)

    
class GameStatus:
    def __init__(self):
        self.players = [
            Player('Human'),
            Player('AI'),
        ]

        self.round_scores = {p: 0 for p in self.players}
        self.total_scores = {p: 0 for p in self.players}
        self.first_player = self.players[0]

    def players(self):
        return self._players(first_player=self.first_player)
    
    def _players(self, first_player):
        players_count = len(self.players)
        start_idx = self.players.find(first_player)
        for i in range(start_idx, players_count):
            yield self.players[i]
            
        if start == 0:
            break    
                    
        for i in range(0, start_idx):
            yield self.players[i]

            
class Player:
    def __init__(self, name):
        self.name = name

    
        
class RoundState(GameState):
    def __init__(self, game, status):
        super(RoundState, self).__init__(game)
        self.status = status
        
        
class NewRoundState(RoundState):
    def run(self):
        player = self.status.first_player
        
    
class ExitState(GameState):
    def run(self):
        self.renderer.print('Bye-bye')
        exit(0)



#                 Graphics and Rendering                   #
# -------------------------------------------------------- #

class Renderer:
    def __init__(self, game):
        self.game = game


class ConsoleRenderer(Renderer):
    def __init__(self, game):
        super(ConsoleRenderer, self).__init__(game)
        self.state_renderers = {
            MainMenuState: MainMenuStateConsoleRenderer(self),
            RoundState: RoundConsoleRenderer(self),
            ExitState: StateConsoleRenderer(self),
        }

    def get_state_renderer(self, state):
        state_class = type(state)
        renderer = self.state_renderers[state_class]
        return renderer

    
class StateConsoleRenderer(Renderer):
    def print(self, *args, **kwargs):
        print(*args, **kwargs)


class MainMenuStateConsoleRenderer(StateConsoleRenderer):
    def show_main_menu(self):
        self.print(
            'Main menu\n'
            '=========\n'
            '1 - Start game\n'
            '2 - Exit\n\n'
        )

    def read_main_menu_input(self):
        char_to_action = {
            '1': MainMenuState.ACTION_START_GAME,
            '2': MainMenuState.ACTION_EXIT,
        }
        c = getch()
        return char_to_action.get(c, MainMenuState.ACTION_UNKNOWN)


class RoundConsoleRenderer(StateConsoleRenderer):
    pass


if __name__ == '__main__':
    main()
