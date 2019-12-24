""" players.py file is a file that contains the Player class for the classic
game of Tag. They have targets,they have enemies and can collide. YAY!!
"""
from __future__ import annotations
import random
from typing import List, Tuple, Optional, Set
from trees import OutOfBoundsError


class Player:
    """ Player is a virtual player in a game.

    === Instance Attributes ===

    All player attributes are private.

    === Private Attributes ===
    _name: The name of a player.

    _location: The coordinates of the current location of a player on a
    2-dimensional grid.

    _colour: The color associated with a player.

    _vision: The distance a player can see in any direction, relative to the
    units on the game grid.

    _speed: The number of steps a player can move in a single turn, relative
    to the units on the game grid.

    _game: A reference to the game which this player is a part of.

    _points: Total number of points of the player.

    _targets: A list of player names that this player actively targets

    _enemies: A list of player names that this player actively avoids

    _direction: A direction that this player faces and moves towards.


    === Representation Invariants ===
    - the <_location> of a player must be within the bounds of the game grid

    - <_vision>, <_points> and <_speed> are all >= 0.

    - the <_colour> of a player must belong to the set
    {'green', 'purple', 'random'}.

    - the <_points> of a player are 0 immediately after initialization.

    - any players in <_targets> cannot simultaneously belong to the list of
    <_enemies> and vice versa.

    - the <_direction> of a player must belong to th set {'N', 'S', 'E', 'W'}.
    """
    _name: str
    _location: Tuple[int, int]
    _colour: str
    _vision: int
    _speed: int
    _game: 'Game'
    _points: int
    _targets: List[str]
    _enemies: List[str]
    _direction: str

    def __init__(self, name: str, vision: int, speed: int, game: 'Game',
                 colour: str, location: Tuple[int, int]) -> None:
        """ Initializes a player according to its <_name>, <_vision>, <_speed>
        and <_colour> (correlating to name , vision , speed and colour ).
        Also assigns the player a <_location> on the <_game> grid (from
        location and game) within self . Preconditions

        === DocTests ===
        >>> player = Player('ethan', 1, 2, game, 'green', (100, 100))
        """
        self._name = name
        self._location = location
        self._colour = colour
        self._vision = vision
        self._speed = speed
        self._game = game
        self._points = 0
        self._targets = []
        self._enemies = []
        self._direction = 'N'

    def set_colour(self, colour: str) -> None:
        """ set_colour changes the <_colour> of the player to one of
        {'green', 'purple', 'random'} according to colour in self .

        === Preconditions ===
        Fails silently if colour does not belong to this set.

        === DocTests ===
        >>> player = Player('ethan', 1, 2, game, 'green', (100, 100))
        >>> player._colour
        'green'
        >>> player.set_colour('purple')
        >>> player._colour
        'purple'
        """
        if colour in ['green', 'purple', 'random']:
            self._colour = colour

    def increase_points(self, points: int) -> None:
        """ increase_points increases the <_points> of the player by points ,
        a non-negative parameter in self .

         === Preconditions ===
         Fails silently if points is negative.

        === DocTests ===
        >>> player = Player('ethan', 1, 2, game, 'green', (100, 100))
        >>> player.get_points()
        0
        >>> player.increase_points(2)
        >>> player.get_points()
        2
         """
        if self._points + points >= 0:
            self._points += points

    def get_points(self) -> int:
        """ get_points returns the <_points> of a player in self .
        Preconditions

        === DocTests ===
        >>> player = Player('ethan', 1, 2, game, 'green', (100, 100))
        >>> player.get_points()
        0
         """
        return self._points

    def select_target(self, name: str) -> None:
        """ select_target adds name to a player's <_targets> list in self .

        === Preconditions ===
        This parameter must be
        unique from any name in <_enemies> and the player's own <_name>,
        otherwise it fails silently.

        === DocTests ===
        >>> player = Player('ethan', 1, 2, game, 'green', (100, 100))
        >>> player.get_targets()
        []
        >>> player.select_target('john')
        >>> player.get_targets()
        ['john']
         """
        if name not in self._enemies and name != self._name:
            self._targets.append(name)

    def ignore_target(self, name: str) -> None:
        """ ignore_target removes name from a player's <_targets> list on the
        condition that it belong to <_targets>, otherwise it fails silently
        in self . Preconditions

        === DocTests ===
        >>> player = Player('ethan', 1, 2, game, 'green', (100, 100))
        >>> player.get_targets()
        []
        >>> player.select_target('john')
        >>> player.get_targets()
        ['john']
        >>> player.ignore_target('john')
        >>> player.get_targets()
        []
        """
        if name in self._targets:
            self._targets.remove(name)

    def get_targets(self) -> List[str]:
        """ get_targets returns a player's <_targets> list from self .
        Preconditions

        === DocTests ===
         >>> player = Player('ethan', 1, 2, game, 'green', (100, 100))
        >>> player.get_targets()
        []
         """
        return self._targets

    def select_enemy(self, name: str) -> None:
        """ select_enemy adds name to a player's <_enemies> list in self .

        === Preconditions ===
        This parameter must be unique from any name in <_targets> and the
        player's own <_name>, otherwise it fails silently.

        === DocTests ===
        >>> player = Player('ethan', 1, 2, game, 'green', (100, 100))
        >>> player.get_enemies()
        []
        >>> player.select_enemy('john')
        >>> player.get_enemies()
        ['john'] """

        if name not in self._targets and name != self._name:
            self._enemies.append(name)

    def ignore_enemy(self, name: str) -> None:
        """ ignore_enemy removes name from a player's <_enemies> list in self .

        === Preconditions ===
        name belongs to <_enemies>, otherwise it fails silently.

        === DocTests ===
        >>> player = Player('ethan', 1, 2, game, 'green', (100, 100))
        >>> player.get_enemies()
        []
        >>> player.select_enemy('john')
        >>> player.get_enemies()
        ['john']
        >>> player.ignore_enemy('john')
        >>> player.get_enemies()
        []
        """

        if name in self._enemies:
            self._enemies.remove(name)

    def get_enemies(self) -> List[str]:
        """ get_enemies returns a player's <_enemies> list in self .
        Preconditions

        >>> player = Player('ethan', 1, 2, game, 'green', (100, 100))
        >>> player.get_enemies()
        []
         """

        return self._enemies

    def reverse_direction(self) -> None:
        """ reverse_direction changes the <_direction> of a player so that they
        face in the exact opposite direction in self .
        Preconditions

        === DocTests ===
         >>> player = Player('ethan', 1, 2, game, 'green', (100, 100))
         >>> player._direction
         'N'
         >>> player.reverse_direction()
         >>> player._direction
         'S'
         """
        if self._direction == 'N':
            self._direction = 'S'
        elif self._direction == 'S':
            self._direction = 'N'
        elif self._direction == 'E':
            self._direction = 'W'
        elif self._direction == 'W':
            self._direction = 'E'

    def set_speed(self, speed: int) -> None:
        """ set_speed changes the player's <_speed> to speed in self .

         === Preconditions ===
         speed is a positive integer.

        === DocTests ===
         >>> player = Player('ethan', 1, 2, game, 'green', (100, 100))
         >>> player._speed
         2
         >>> player.set_speed(3)
         >>> player._speed
         3
         """
        if speed >= 0:
            self._speed = speed

    def _helper_tally(self, name_list1: List[str], name_list2: List[str],
                      first_d: str, second_d: str) -> List[int]:
        """ _helper_tally is helper tally
        It takes two lists of the two directions as well as the two
        directions, name_list1 name_list2 first_d second_d and then
        tallies the number of people as a target and enemy in each direction.
        Preconditions
        """
        N = 0
        E = 0
        S = 0
        W = 0
        for person in self._targets:
            if person in name_list1:
                if 'N' in first_d:
                    N += 1
                if 'E' in first_d:
                    E += 1
                if 'S' in first_d:
                    S += 1
                if 'W' in first_d:
                    W += 1
            if person in name_list2:
                if 'N' in second_d:
                    N += 1
                if 'E' in second_d:
                    E += 1
                if 'S' in second_d:
                    S += 1
                if 'W' in second_d:
                    W += 1
        for person in self._enemies:
            if person in name_list1:
                if 'N' not in first_d:
                    N += 1
                if 'E' not in first_d:
                    E += 1
                if 'S' not in first_d:
                    S += 1
                if 'W' not in first_d:
                    W += 1
            if person in name_list2:
                if 'N' not in second_d:
                    N += 1
                if 'E' not in second_d:
                    E += 1
                if 'S' not in second_d:
                    S += 1
                if 'W' not in second_d:
                    W += 1
        return [N, E, S, W]

    def next_direction(self) -> Set[str]:
        """ Updates the <_direction> of the player for the next time the
        <player.move> method is called. This direction is determined by the
        relative number of visible targets and enemies. Likewise returns a set
        of all equally good directions to move towards for the
        player. In accordance with the class RI's, <_direction> will belong
        to the set {'N', 'S', 'E', 'W'}. next_direction in self
        Preconditions

        === DocTests ===
        >>> player1 = Player('ethan', 1, 2, game, 'green', (100, 100))
        >>> player1.next_direction()
        >>> player1._direction in ['N', 'E', 'W', 'S']
        True
        """
        dirs = ['NW', 'NE', 'SW', 'SE']
        first_d = random.choice(dirs)
        dirs.remove(first_d)
        second_d = random.choice(dirs)
        people_first = self._game.field.names_in_range(self._location, first_d,
                                                       self._vision)
        people_second = self._game.field.names_in_range(self._location,
                                                        second_d, self._vision)
        dirs = self._helper_tally(people_first, people_second, first_d,
                                  second_d)
        N = dirs[0]
        E = dirs[1]
        S = dirs[2]
        W = dirs[3]
        dirs.sort()
        i = len(dirs) - 1
        while i > 0:
            if dirs[i] > dirs[i - 1]:
                break
            i -= 1
        result = dirs[i]
        last = set()
        if result == N:
            last.add('N')
        if result == E:
            last.add('E')
        if result == W:
            last.add('W')
        if result == S:
            last.add('S')
        self._direction = random.choice(tuple(last))
        return last

    def move(self) -> None:
        """ move moves the player in self towards <_direction> by the
        steps of <_speed>. Updates the players <_location> accordingly. If the
        movement would move the player out of bounds, reverse <_direction> and
        continue with the move. <_direction> should not change until
        <player.next_direction> is called again.
        Preconditions

         >>> player = Player('ethan', 1, 2, game, 'green', (100, 100))
         >>> player.move()
         >>> player._location
         (98, 100)
        """
        if self._direction == 'N':
            points = (self._location[0], self._location[1] - self._speed)
            new_spot = points
        elif self._direction == 'S':
            points = (self._location[0], self._location[1] + self._speed)
            new_spot = points
        elif self._direction == 'W':
            points = (self._location[0] - self._speed, self._location[1])
            new_spot = points
        else:
            points = (self._location[0] + self._speed, self._location[1])
            new_spot = points
        try:
            self._game.field.insert(self._name, new_spot)
            self._game.field.remove_point(self._location)
            self._location = new_spot
        except OutOfBoundsError:
            self.reverse_direction()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(
        config={'extra-imports': ['typing', 'random', 'games', 'trees'],
                'disable': ['R0913', 'R0902', 'W0611', 'R1710', 'R1702']})
