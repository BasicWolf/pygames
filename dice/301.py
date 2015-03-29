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
#     next round, or stop rolling and skip all the next turns.
# 2.5 The round ends when a single player left or when all remaining players
#     decide to skip the round. In this case a player with highest summary
#     points wins the game. The game is considered a draw and 'no-win' for
#     players if all summary points are equal.

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
            AiPlayer('Alice', 1),
            AiPlayer('Bob', 2),
            AiPlayer('Ed', 3),
        ]

        self.score = {p: 0 for p in self.players}
        self.next_round_player = self.players[0]

    def update_score(self, player):
        self.score[player] += 1


class Player:
    def __init__(self, name):
        self.name = name


class HumanPlayer(Player):
    pass



class AiPlayer(Player):
    def __init__(self, name, risk=1):
        super(AiPlayer, self).__init__(name)
        self.risk = risk
        
    def check_stops(self, turn_state):
        status = turn_state.status
        my_score = status.scores[self]
        safe_boundary = Game.MAX_ROUND_SCORE - Game.MAX_DICE_VALUE // 2 + self.risk
        my_score_biggest = all(my_score >= status.scores[p]
                               for p in status.players
                               if p != self)
        return my_score_biggest and my_score >= safe_boundary

    def __str__(self):
        return 'AiPlayer [name: %s]' % self.name

    def __repr__(self):
        return str(self)

    
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

    def __init__(self, *args, **kwargs):
        try:
            s = kwargs['state']
            game, status = s.game, s.status
        except KeyError:
            game, status = args

        super(RoundState, self).__init__(game)
        self.status = status


class RoundStatus:
    def __init__(self, game):
        self.game = game
        self.players = list(game.status.players)
        self.stopped_players = set()
        self.scores = {p: 0 for p in self.players}
        self._player = game.status.next_round_player
        self.winner = None
        self.complete = False

    @property
    def player(self):
        return self._player

    def advance_player(self):
        self._player = self._get_next_player()

    def _get_next_player(self):
        player = self.player
        players = self.players

        player_idx = players.index(player)
        next_player_idx = (player_idx + 1) % len(players)
        return players[next_player_idx]

    def update_score(self, score):
        self.scores[self.player] += score
        self.update()

    def player_stopped(self):
        player = self.player
        self.advance_player()
        self.players.remove(player)
        self.stopped_players.add(player)
        self.update()

    def player_lost(self):
        player = self.player
        self.advance_player()
        self.players.remove(player)

    def complete_with_winner(self, player):
        self.complete = True
        self.winner = player

    def complete_draw(self):
        self.complete = True

    def update(self):
        if len(self.players) == 0:
            if len(self.stopped_players) == 0:
                self.complete_draw()
            elif len(self.stopped_players) == 1:
                self.complete_with_winner(self.stopped_players[0])
            else:
                stopped_players = sorted(self.stopped_players,
                                         key=lambda p: self.scores[p],
                                         reverse=True)
                max_score_player = stopped_players[0]
                max_score = self.scores[max_score_player]
                max_score_won = all(max_score > self.scores[p]
                                    for p in stopped_players[1:])
                if max_score_won:
                    # e.g. [10, 9, 9, ...]
                    self.complete_with_winner()
                else:
                    # e.g. [10, 10, 8, ...]
                    self.complete_draw()

        elif len(self.players) == 1:
            if len(self.stopped_players) == 0:
                # all other players lost, no players stopped
                self.complete_with_winner(self.player)
            else:
                player_score = self.scores[self.player]
                if all(player_score > self.scores[p]
                       for p in self.stopped_players):
                    self.complete_with_winner(self.player)

        elif self.scores[self.player] > Game.MAX_ROUND_SCORE:
            self.player_lost()
        elif self.scores[self.player] == Game.MAX_ROUND_SCORE:
            self.complete_with_winner(self.player)
        else:
            self.advance_player()

class NewRoundState(RoundState):
    def __init__(self, game):
        status = RoundStatus(game)
        super(NewRoundState, self).__init__(game, status)

    def run(self):
        self.renderer.render()
        return RoundTurnStart(state=self)


class RoundTurnStart(RoundState):
    def run(self):
        if self.status.complete:
            return RoundEndState(state=self)
        else:
            return RoundTurnCheckPlayerStops(state=self)


class RoundTurnCheckPlayerStops(RoundState):
    def run(self):
        if self.player_stops():
            self.status.player_stopped()
            return RoundTurnStart(state=self)
        else:
            return RoundTurnRoll(state=self)

    def player_stops(self):
        status = self.status
        player = status.player
        pscore = status.scores[player]
        score_is_biggest = max(status.scores.values()) <= pscore
        score_not_safe = Game.MAX_ROUND_SCORE - pscore  < Game.MAX_DICE_VALUE
        if score_not_safe and score_is_biggest:
            return self.read_player_stops(player)
        else:
            return False

    def read_player_stops(self, player):
        if isinstance(player, HumanPlayer):
            stops = self.renderer.read_human_player_stops(player)
        else:
            stops = player.check_stops(self)
            self.renderer.player_stops(player.name, stops)
        return stops


class RoundTurnRoll(RoundState):
    def run(self):
        self.roll()
        if self.status.complete:
            return RoundEndState(state=self)
        else:
            return RoundTurnStart(state=self)

    def roll(self):
        status = self.status
        player = status.player
        self.renderer.read_roll(player)
        roll_score = randint(1, Game.MAX_DICE_VALUE)
        status.update_score(roll_score)
        total_score = status.scores[player]
        self.renderer.player_rolled(player.name, roll_score, total_score)


class RoundEndState(RoundState):
    def run(self):
        game_status = self.game.status
        game_status.next_round_player = self.status.player
        if self.status.winner is not None:
            self.renderer.render_winner(self.status.winner.name)
            game_status.update_score(self.status.winner)
        self.renderer.render_scores()
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
            RoundTurnCheckPlayerStops: RoundTurnCheckPlayerStopsRenderer,
            RoundTurnRoll: RoundTurnRollRenderer,
            RoundEndState: RoundEndConsoleRenderer,
            ExitState: StateConsoleRenderer,
        }


    def get_state_renderer(self, state):
        state_class = type(state)
        renderer_class = self.state_renderers_classes.get(state_class, Renderer)
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

    def input(self, *args, **kwargs):
        return input(*args, **kwargs)


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
        print('\n\nNew round\n---------\n')


class RoundTurnConsoleRenderer(StateConsoleRenderer):
    def render_win(self, player):
        self.print('{} won!'.format(player.name))

    def render_loose(self, player):
        self.print('{} lost :('.format(player.name))


class RoundTurnRollRenderer(StateConsoleRenderer):
    def read_roll(self, player):
        if isinstance(player, HumanPlayer):
            self.input('\nRoll the dice (press [ENTER])')

    def player_rolled(self, player_name, roll_score, total_rolled):
        self.print('{} rolled: {} [{}]'.format(player_name, roll_score, total_rolled))


class RoundTurnCheckPlayerStopsRenderer(StateConsoleRenderer):
    def player_stops(self, player_name, stops):
        if stops:
            self.print('%s decides to stop' % player_name)
        else:
            self.print('%s rolls the dice' % player_name)

    def read_human_player_stops(self, player):
        prompt = ('{}, would you like to stop rolling the dice? [y/n]'
                  .format(player.name))
        c = self.getch(prompt, 'yn')
        return c == 'y'


class RoundEndConsoleRenderer(StateConsoleRenderer):
    def render_winner(self, player_name):
        self.print('\nThe winner is: %s' % player_name)

    def render_scores(self):
        self.print('Total scores: ')
        status = self.game.status
        for p in status.players:
            self.print('{}: {}'.format(p.name, status.score[p]))

if __name__ == '__main__':
    main()
