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


class GameStatus:
    def __init__(self):
        self.players = [
            HumanPlayer('Human'),
            AiPlayer('AI'),
        ]

        self.total_scores = {p: 0 for p in self.players}
        self.next_round_player = self.players[0]


class Player:
    def __init__(self, name):
        self.name = name


class HumanPlayer(Player):
    pass


class AiPlayer(Player):
    def will_roll(self, turn_state):
        return False


class GameState(metaclass=ABCMeta):
    ACTION_UNKNOWN = 0

    def __init__(self, game):
        self.game = game
        self.renderer = game.renderer.get_state_renderer(self)

    @abstractmethod
    def run(self):
        pass


class MainMenuState(GameState):
    ACTION_START_GAME = 1
    ACTION_EXIT = 2

    def run(self):
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
        self.renderer.render_new_game()
        return NewRoundState(self.game)


class RoundState(GameState):
    status = None
    
    def __init__(self, game, status):
        super(RoundState, self).__init__(game)
        self.status = status

class RoundStatus:
    scores = None
    next_player = None
    lost_players = None
    stopped_player = None

    def __init__(self, game):
        self.game = game
        players = game.status.players
        self.scores = (0, ) * len(players)
        self.next_player = game.status.next_round_player
        self.lost_players = []
        self.stopped_players = []
        
    # def advance_player(self):
    #     self.next_player = next(self.players())

    def players(self, next_player=None):
        next_player = next_player or self.next_player

        players = self.game.status.players
        players_count = len(players)

        start_idx = players.index(next_player)
        for i in range(start_idx, players_count):
            yield players[i]

        if start_idx == 0:
            return

        for i in range(0, start_idx):
            yield players[i]
    

class NewRoundState(RoundState):
    def __init__(self, game):
        status = RoundStatus(game)
        super(NewRoundState, self).__init__(game, status)
        
    def run(self):
        self.reset_scores()
        self.renderer.render()
        return RoundTurnState(self.game, self.status)

    def reset_scores(self):
        self.scores = {p: 0 for p in self.game.status.players}
        self.next_player = self.game.status.next_round_player
        self.lost_players = set()


class RoundTurnState(RoundState):
    ACTION_UNKNOWN = 0
    ACTION_WILL_ROLL = 1
    
    def run(self):
        for p in self.status.players():
            if self.will_player_roll(p):
                self.roll(p)
                self.check_player_winloose_conditions(p)

    def roll(self, player):
        score = randint(1, 6)
        self.scores[p] += score

    def will_player_roll(self, player):
        if isinstance(player, HumanPlayer):
            will_roll = self.renderer.will_human_player_roll(player)
        else:
            will_roll = player.will_roll(self)
            self.renderer.will_ai_player_roll(ai_will_roll)
        return will_roll


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
        self.state_renderers_classes = {
            MainMenuState: MainMenuStateConsoleRenderer,
            NewGameState: NewGameStateConsoleRenderer,
            NewRoundState: NewRoundStateConsoleRenderer,
            RoundTurnState: RoundTurnConsoleRenderer,
            ExitState: StateConsoleRenderer,
        }


    def get_state_renderer(self, state):
        state_class = type(state)
        renderer_class = self.state_renderers_classes[state_class]
        return renderer_class(self.game)


class StateConsoleRenderer(Renderer):
    def print(self, *args, **kwargs):
        print(*args, **kwargs)

    def getch(self, prompt='', keys=''):
        while 1:
            self._print_prompt(prompt)
            c =  getch()
            if keys == '':
                return c
            else:
                if c in keys:
                    return c

    def _print_prompt(self, prompt):
        if prompt != '':
            self.print(prompt)

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
        c = self.getch()
        return char_to_action.get(c, MainMenuState.ACTION_UNKNOWN)


class NewGameStateConsoleRenderer(StateConsoleRenderer):
    def render_new_game(self):
        players_count = len(self.game.status.players)
        self.print('\nStarting a new game with %d players\n' % players_count)


class RoundConsoleRenderer(StateConsoleRenderer):
    pass

class NewRoundStateConsoleRenderer(StateConsoleRenderer):
    def render(self):
        print('\nNew round\n')

class RoundTurnConsoleRenderer(StateConsoleRenderer):
    def will_human_player_roll(self, player):
        c = self.getch('%s, will you roll the dice? [y/n]' % player.name, 'yn')
        return c == 'y'

    def will_ai_player_roll(self, ai_will_roll):
        if ai_will_roll:
            self.print('AI decides to roll the dice')
        else:
            self.print('AI will not roll the dice')


if __name__ == '__main__':
    main()
