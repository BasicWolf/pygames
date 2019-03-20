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
    MAX_DICE_VALUE = 6
    MAX_ROUND_SCORE = 13

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

        self.wins = {p: 0 for p in self.players}
        self.next_round_player = self.players[0]

    def player_wins(self, player):    
        self.wins[player] += 1
        

class Player:
    def __init__(self, name):
        self.name = name


class HumanPlayer(Player):
    pass


class AiPlayer(Player):
    def check_stops(self, turn_state):
        status = turn_state.status
        my_score = status.scores[self]
        safe_boundary = Game.MAX_ROUND_SCORE - Game.MAX_DICE_VALUE // 2
        my_score_biggest = all(my_score > status.scores[p] for p in status.players
                               if p != self)
        return my_score_biggest and my_score >= safe_boundary


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
    def __init__(self, game):
        self.game = game
        self.players = list(game.status.players)
        self.scores = {p: 0 for p in self.players}
        self._turn_player = game.status.next_round_player
        self.win_player = None

    def advance_player(self):
        self._turn_player = self._get_next_player()

    def _get_next_player(self):
        player = self.turn_player
        players = self.players

        player_idx = players.index(player)
        next_player_idx = (player_idx + 1) % len(players)
        return players[next_player_idx]

    def update_score(self, score):    
        self.scores[self._turn_player] += score

    def player_stops(self):
        player = self._turn_player
        self.advance_player()
        self.players.remove(player)

    def player_wins(self):
        self.win_player = self._turn_player
        
    def player_looses(self):
        player = self._turn_player
        self.advance_player()
        self.players.remove(player)
        
    @property
    def turn_player(self):
        return self._turn_player


class NewRoundState(RoundState):
    def __init__(self, game):
        status = RoundStatus(game)
        super(NewRoundState, self).__init__(game, status)

    def run(self):
        self.renderer.render()
        return RoundTurnState(self.game, self.status)


class RoundTurnState(RoundState):
    ACTION_UNKNOWN = 0

    def run(self):
        player = self.status.turn_player

        # Only one player left in current round
        if (len(self.status.players) == 1):
            self.status.player_wins()
            self.renderer.render_win(player)            
            return RoundEndState(self.game, self.status)
        
        player_score = self.status.scores[player]
        player_close_to_score_boundary = (
            Game.MAX_ROUND_SCORE - player_score  < Game.MAX_DICE_VALUE)

        if player_close_to_score_boundary and self.read_player_stops(player):
            self.status.player_stops()
            return self.next_turn()

        roll_score = self.roll()
        total_score = player_score + roll_score

        self.renderer.render_player_rolled(player, roll_score, total_score)

        if self._is_player_won(player):
            self.status.player_wins()
            self.renderer.render_win(player)
            return self.end_round()
        elif self._is_player_lost(player):
            self.renderer.render_loose(player)
            self.status.player_looses()
        else:
            self.status.advance_player()

        # no winners (e.g. even, or all lost)
        if (len(self.status.players) == 0):
            return self.end_round()
        
        return self.next_turn()

    def roll(self):
        roll_score = randint(1, Game.MAX_DICE_VALUE)
        self.status.update_score(roll_score)
        return roll_score

    def read_player_stops(self, player):
        if isinstance(player, HumanPlayer):
            stops = self.renderer.read_human_player_stops(player)
        else:
            stops = player.check_stops(self)
            self.renderer.render_ai_player_stops(stops)
        return stops

    def _is_player_won(self, player):
        return self.status.scores[player] == Game.MAX_ROUND_SCORE

    def _is_player_lost(self, player):
        return self.status.scores[player] > Game.MAX_ROUND_SCORE

    def next_turn(self):
        return RoundTurnState(self.game, self.status)

    def end_round(self):
        return RoundEndState(self.game, self.status)        

class RoundEndState(RoundState):
    def run(self):
        game_status = self.game.status
        game_status.next_round_player = self.status.turn_player
        if self.status.win_player != None:
            game_status.player_wins(self.status.win_player)
        self.renderer.render()
        return NewRoundState(self.game)

    
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
            RoundEndState: RoundEndConsoleRenderer,
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
        c = self.getch('', '12')
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
    def read_human_player_stops(self, player):
        c = self.getch('%s, would you like to stop rolling the dice? [y/n]' % player.name, 'yn')
        return c == 'y'

    def render_ai_player_stops(self, ai_stops):
        if ai_stops:
            self.print('AI decides to stop')
        else:
            self.print('AI rolls the dice')

    def render_player_rolled(self, player, roll_score, total_rolled):
        self.print('{} rolled: {} [{}]'.format(player.name, roll_score, total_rolled))

    def render_win(self, player):
        self.print('{} won!'.format(player.name))

    def render_loose(self, player):
        self.print('{} lost :('.format(player.name))

        
class RoundEndConsoleRenderer(StateConsoleRenderer):
    def render(self):
        self.print('Total scores: ')
        status = self.game.status
        for p in status.players:
            self.print('{}: {}'.format(p.name, status.wins[p]))

if __name__ == '__main__':
    main()
