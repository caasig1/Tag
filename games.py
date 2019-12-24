""" games.py file is a file that contains different variations of the classic
Tag Game.
It has a Normal Tag game, Zombie Tag, and Elimination Tag!! So much fun!!
"""
from __future__ import annotations
import random
from typing import Dict, Union, Optional
from players import Player
from trees import QuadTree, TwoDTree


class Game:
    """ This is the Parent class for all games.
    It is empty because all its methods raise a NotImplementedError
    """

    def handle_collision(self, player1: str, player2: str) -> None:
        """ Perform some action when <player1> and <player2> collide in self """
        raise NotImplementedError

    def check_for_winner(self) -> Optional[str]:
        """ Return the name of the player or group of players that have
        won the game, or None if no player has won yet in self """
        raise NotImplementedError


class Tag(Game):
    """ This is a game of classic Tag
    It creates a game full of players that are placed onto a field.

    === Attributes ===
    _players : A dictionary mapping the names of players to their Player
        instances
    field : A tree that stores the location of all players in _players
    _it : The name of the player in _players that is currently ‘it’
    _duration : The amount of time before the game eliminates some more players

    === Representation Invariants ===
    The player who is ‘it’ should be purple, all other players should be green.

    === DocTests ===
    >>> game = Tag(10, QuadTree((250, 250)), 5, 4, 3)
    >>> game._duration == 5
    True
    >>> type(game.field) == QuadTree
    True
    >>> game._it in game.field
    True
    """
    _players: Dict[str, Player]
    field: Union[QuadTree, TwoDTree]
    _it: str
    _duration: int

    def __init__(self, n_players: int,
                 field_type: Union[QuadTree, TwoDTree],
                 duration: int,
                 max_speed: int,
                 max_vision: int) -> None:
        """ Initialize new Game instance onto a field of field_type in self

        === Preconditions ===
        n_players must be > 0
        duration max_speed and max_vision must be > 0

        === DocTests ===
        >>> game = Tag(10, QuadTree((250, 250)), 5, 4, 3)
        >>> game._players[game._it]._colour == 'purple'
        True
        """
        self._players = {}
        self.field = field_type
        self._duration = duration
        for i in range(n_players):
            vision = random.randint(0, max_vision)
            speed = random.randint(1, max_speed)
            location = (random.randint(0, 500), random.randint(0, 500))
            while self.field.contains_point(
                    location) or self.field.names_in_range(
                        (location[0] + 10, location[1] + 10), 'NW', 10) != []:
                location = (random.randint(0, 500), random.randint(0, 500))
            self._players[str(i)] = Player(str(i), vision, speed, self, 'green',
                                           location)
            self.field.insert(str(i), location)
        self._it = random.choice(list(self._players.keys()))
        self._players[self._it].set_colour('purple')
        for name in self._players:
            if name != self._it:
                self._players[name].select_enemy(self._it)
            else:
                everyone_else = list(self._players.keys())
                everyone_else.remove(name)
                for person in everyone_else:
                    self._players[name].select_target(person)

    def _helper_changed_it(self, old_it: str, new_it: str) -> None:
        """ _helper_changed_it is helper changed it
        It changes who is it, from old_it to new_it and takes self
        """
        for name in self._players:
            if name != new_it:
                self._players[name].select_enemy(new_it)
                self._players[name].ignore_enemy(old_it)
                if name == old_it:
                    for player in list(self._players.keys()):
                        self._players[name].ignore_target(player)
            else:
                for player in list(self._players.keys()):
                    self._players[name].select_target(player)
                self._players[name].ignore_enemy(old_it)

    def handle_collision(self, player1: str, player2: str) -> None:
        """ Perform some action when <player1> and <player2> collide on self
        Both players reverses the direction they are moving in.
        If one of the players is ‘it’, the other player becomes ‘it’ and its
            points increase by 1. handle_collision on self

        === Preconditions ===
        player1 and player2 are players currently in the game

        === DocTests ===
        >>> game = Tag(10, QuadTree((250, 250)), 5, 4, 3)
        >>> game.handle_collision(str(int(game._it) + 1), str(int(game._it)))
        """
        if self._it == player1:
            self._players[self._it].set_colour('green')
            self._it = player2
            self._players[self._it].set_colour('purple')
            self._players[player2].increase_points(1)
            self._players[player2].reverse_direction()
            self._players[player1].reverse_direction()
            self._helper_changed_it(player1, player2)
        elif self._it == player2:
            self._players[self._it].set_colour('green')
            self._it = player1
            self._players[self._it].set_colour('purple')
            self._players[player1].increase_points(1)
            self._players[player1].reverse_direction()
            self._players[player2].reverse_direction()
            self._helper_changed_it(player2, player1)
        else:
            self._players[player1].reverse_direction()
            self._players[player2].reverse_direction()

    def check_for_winner(self) -> Optional[str]:
        """ Return the name of the player or group of players that have
        won the game, or None if no player has won yet on self
        If there are more than 2 players left then return None and eliminate
        tagged players.
        If there are 2 players left, the one who is not 'it' wins and
        if there is only 1 player left then they win. Preconditions

        === DocTests ===
        >>> game = Tag(10, QuadTree((250, 250)), 5, 4, 3)
        >>> game.check_for_winner()
        """
        if len(self._players) > 2:
            for player in self._players:
                if self._players[
                        player].get_points() > 0 and self._it != player:
                    self._players.pop(player)
                    self.field.remove(player)
            return None
        else:
            if len(self._players) == 1:
                return list(self._players.keys())[0]
            else:
                self._players.pop(self._it)
                return list(self._players.keys())[0]


class ZombieTag(Game):
    """ This is a game of Zombie Tag, ZombieTag
    It creates a game full of players that are placed onto a field.

    === Attributes ===
    _humans : A dictionary mapping the names of human players to their Player
        instances
    _zombies : A dictionary mapping the names of zombie players to their Player
        instances
    field : A tree that stores the location of all players in _players
    _duration : The amount of time before the game eliminates some more players

    === Representation Invariants ===
    All zombies are purple, all humans are green.

    === DocTests ===
    >>> game = ZombieTag(10, QuadTree((250, 250)), 5, 4, 3)
    >>> game._duration == 5
    True
    >>> type(game.field) == QuadTree
    True
    """
    _humans: Dict[str, Player]
    _zombies: Dict[str, Player]
    field: Union[QuadTree, TwoDTree]
    _duration: int

    def __init__(self, n_players: int,
                 field_type: Union[QuadTree, TwoDTree],
                 duration: int,
                 max_speed: int,
                 max_vision: int) -> None:
        """ Initialize new Game instance with n_players as humans and one
        zombie in self on a field of field_type and size as specified

        === Preconditions ===
        n_players must be > 0
        duration max_speed and max_vision must be > 0

        === DocTests ===
        >>> game = ZombieTag(10, QuadTree((250, 250)), 5, 4, 3)
        >>> game._zombies['0']._colour == 'purple'
        True
        """
        self._duration = duration
        self.field = field_type
        self._humans = {}
        self._zombies = {}

        for i in range(n_players):
            loc = (250, 250)
            v = random.randint(0, max_vision)
            s = random.randint(0, max_speed)
            while self.field.contains_point(loc) or self.field.names_in_range(
                    (loc[0] + 10, loc[1] + 10), 'NW', 10) != []:
                loc = (random.randint(0, 500), random.randint(0, 500))

            self._humans[str(i)] = Player(str(i), v, s, self, 'green', loc)
            self.field.insert(str(i), loc)
        z_loc = (251, 251)
        while self.field.contains_point(z_loc):
            z_loc = (random.randint(0, 500), random.randint(0, 500))

        self._zombies[str(n_players)] = Player(str(n_players), max_vision, 1,
                                               self, 'purple', z_loc)
        self.field.insert(str(n_players), z_loc)

        for j in self._humans:
            self._zombies[str(n_players)].select_target(j)
            self._humans[j].select_enemy(str(n_players))

    def handle_collision(self, player1: str, player2: str) -> None:
        """" Perform some action when <player1> and <player2> collide on self
        Both players reverses the direction they are moving in.
        If one of the players is a zombie and the other is a human,
            the other player transforms and its speed is set to 1.
            handle_collision on self

        === Preconditions ===
        player1 and player2 are players currently in the game

        === DocTests ===
        >>> game = ZombieTag(10, QuadTree((250, 250)), 5, 4, 3)
        >>> game.handle_collision('0', '9')
        """
        if player1 in self._zombies.keys() and player2 in self._zombies.keys():
            self._zombies[player1].reverse_direction()
            self._zombies[player2].reverse_direction()
        elif player1 in self._humans.keys() and player2 in self._humans.keys():
            self._humans[player1].reverse_direction()
            self._humans[player2].reverse_direction()
        elif player1 in self._zombies.keys() and player2 in self._humans.keys():
            self._h_to_z(player2)
            self._zombies[player1].reverse_direction()
            self._zombies[player2].reverse_direction()
        elif player2 in self._zombies.keys() and player1 in self._humans.keys():
            self._h_to_z(player1)
            self._zombies[player1].reverse_direction()
            self._zombies[player2].reverse_direction()

    def check_for_winner(self) -> Optional[str]:
        """ Return the name of the player or group of players that have
        won the game, or None if no player has won yet on self
        If there are humans left, humans win.
        Otherwise, zombies win. Preconditions

        === DocTests ===
        >>> game = ZombieTag(10, QuadTree((250, 250)), 5, 4, 3)
        >>> game.check_for_winner()
        """
        if not self._humans:
            return 'zombies'
        else:
            return 'humans'

    def _h_to_z(self, player: str) -> None:
        """ _h_to_z is h to z
        It changes player from human to zombie in self"""
        for j in list(self._zombies.keys()):
            self._humans[player].ignore_enemy(j)
            self._zombies[j].ignore_target(player)
        self._zombies[player] = self._humans[player]
        del self._humans[player]
        self._zombies[player].set_speed(1)
        self._zombies[player].set_colour('purple')
        for i in list(self._humans.keys()):
            self._zombies[player].select_target(i)


class EliminationTag(Game):
    """ This is a game of Elimination Tag, EliminationTag
    It creates a game full of players that are placed onto a field.
    Each player has a target and someone targeting them who they do not know.
    Last person standing wins
    In this game, every player has exactly one other player they are trying to
    tag. Once a player tags their target, their target is eliminated and
    they now try to tag their target’s target.

    === Attributes ===
    _players : A dictionary mapping the names of players to their Player
    instances
    field : A tree that stores the location of all players in _players

    === Representation Invariants ===
    When there is eventually only two players left, the winner is decided as
    the player who has eliminated the most other players. If both players have
    eliminated the same number, the game ends in a tie.

    === DocTests ===
    >>> game = ZombieTag(10, QuadTree((250, 250)), 5, 4, 3)
    >>> game._duration == 5
    True
    >>> type(game.field) == QuadTree
    True
    """
    _players: Dict[str, Player]
    field: Union[QuadTree, TwoDTree]

    def __init__(self, n_players: int,
                 field_type: Union[QuadTree, TwoDTree],
                 max_speed: int,
                 max_vision: int) -> None:
        """ Initialize new Game instance with n_players in self on a field of
        field_type and size as specified.
        In alphabetical order, each next player is the previous player's target

        === Preconditions ===
        n_players must be > 0
        max_speed and max_vision must be > 0

        === DocTests ===
        >>> game = EliminationTag(10, QuadTree((250, 250)), 4, 3)
        >>> game._players['0']._colour == 'random'
        True
        """
        self._players = {}
        self.field = field_type
        for i in range(n_players):
            vision = random.randint(0, max_vision)
            speed = random.randint(1, max_speed)
            location = (random.randint(0, 500), random.randint(0, 500))
            while self.field.contains_point(
                    location) or self.field.names_in_range(
                        (location[0] + 10, location[1] + 10), 'NW', 10) != []:
                location = (random.randint(0, 500), random.randint(0, 500))
            self._players[str(i)] = Player(str(i), vision, speed, self,
                                           'random', location)
            self.field.insert(str(i), location)
            if i != n_players - 1:
                self._players[str(i)].select_target(str(i + 1))
            else:
                self._players[str(i)].select_target(str(0))

    def handle_collision(self, player1: str, player2: str) -> None:
        """" Perform some action when <player1> and <player2> collide on self
        Both players reverses the direction they are moving in if neither of
        them are the other's target.
        Otherwise, eliminate the player being targeted and increase the points
        of the attacker by 1. The person eliminated's target is the attacker's
        new target

        === Preconditions ===
        player1 and player2 are players currently in the game

        === DocTests ===
        >>> game = EliminationTag(10, QuadTree((250, 250)), 5, 4, 3)
        >>> game.handle_collision('0', '1')
        """
        if player1 in self._players[player2].get_targets():
            next_target = self._players[player1].get_targets()
            self._players[player2].select_target(next_target[0])
            self._players[player2].ignore_target(player1)
            self._players[player2].increase_points(1)
            self.field.remove(player1)
            self._players.pop(player1)
        elif player2 in self._players[player1].get_targets():
            next_target = self._players[player2].get_targets()
            self._players[player1].select_target(next_target[0])
            self._players[player1].ignore_target(player2)
            self._players[player1].increase_points(1)
            self.field.remove(player2)
            self._players.pop(player2)
        else:
            self._players[player2].reverse_direction()
            self._players[player1].reverse_direction()

    def check_for_winner(self) -> Optional[str]:
        """ Return the name of the player or group of players that have
        won the game, or None if no player has won yet on self
        Return the person with the most points. If there is a tie, return
        None. Preconditions

        === DocTests ===
        >>> game = EliminationTag(10, QuadTree((250, 250)), 5, 4, 3)
        >>> game.check_for_winner()
        """
        highest = 0
        names = []
        for player in self._players:
            if self._players[player].get_points() > highest:
                highest = self._players[player].get_points()
                names = [player]
            elif self._players[player].get_points() == highest:
                names.append(player)
        if len(names) > 1:
            return None
        else:
            return names[0]


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(
        config={'extra-imports': ['random', 'typing', 'players', 'trees'],
                'disable': ['R0913', 'R0902', 'W0611', 'R1710', 'R1702']})
