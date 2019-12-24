""" trees.py file is a file that has the Tree classes
It contains Tree, QuadTree and TwoDTree
"""
from __future__ import annotations
from typing import Optional, List, Tuple, Dict


class OutOfBoundsError(Exception):
    """ This is the OutOfBoundsError which means that a player is
    Out of bounds and has an error."""
    pass


class Tree:
    """ Tree is the parent class of QuadTree and TwoDTree. It is completely
    empty because everything is not implemented yet."""
    def __contains__(self, name: str) -> bool:
        """ Return True if a player named <name> is stored in this tree.
        __contains__ checks if name is contained in self
        Runtime: O(n)
        """
        raise NotImplementedError

    def contains_point(self, point: Tuple[int, int]) -> bool:
        """ Return True if a player at location <point> is stored in this tree.
        contains_point checks if point is in self
        Runtime: O(log(n))
        """
        raise NotImplementedError

    def insert(self, name: str, point: Tuple[int, int]) -> None:
        """Insert a player named <name> into this tree at point <point>.
        insert a point and name into self
        Raise an OutOfBoundsError if <point> is out of bounds.

        Raise an OutOfBoundsError if moving the player would place the player at
        exactly the same coordinates of another player in the Tree (before
        moving the player).

        Runtime: O(log(n))
        """
        raise NotImplementedError

    def remove(self, name: str) -> None:
        """ Remove information about a player named <name> from this tree.
        remove a name from self
        Runtime: O(n)
        """
        raise NotImplementedError

    def remove_point(self, point: Tuple[int, int]) -> None:
        """ Remove information about a player at point <point> from this tree.
        remove_point removes a point in self
        Runtime: O(log(n))
        """
        raise NotImplementedError

    def move(self, name: str, direction: str, steps: int) -> Optional[
            Tuple[int, int]]:
        """ Return the new location of the player named <name> after moving it
        in the given <direction> by <steps> steps.
        move a name in a direction by a number of steps in self
        Raise an OutOfBoundsError if this would move the player named
        <name> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player
        at exactly the same coordinates of another player in the Tree (before
        moving the player).

        Runtime: O(n)

        === precondition ===
        direction in ['N', 'S', 'E', 'W']
        """
        raise NotImplementedError

    def move_point(self, point: Tuple[int, int], direction: str, steps: int) ->\
            Optional[Tuple[int, int]]:
        """ Return the new location of the player at point <point> after moving
        it in the given <direction> by <steps> steps.
        move_point moves a point in a direction by a number of steps in self
        Raise an OutOfBoundsError if this would move the player at point
        <point> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at
        exactly the same coordinates of another player in the Tree (before
        moving the player).

        Moving a point may require the tree to be reorganized. This method
        should do the minimum amount of tree reorganization possible to move the
        given point properly.

        Runtime: O(log(n))

        === precondition ===
        direction in ['N', 'S', 'E', 'W']

        """
        raise NotImplementedError

    def names_in_range(self, point: Tuple[int, int], direction: str,
                       distance: int) -> List[str]:
        """ Return a list of names of players whose location is in the
        <direction> relative to <point> and whose location is within <distance>
        along both the x and y axis.
        names_in_range uses a point and searches in a direction for a certain
        distance in self
        For example: names_in_range((100, 100), 'SE', 10) should return the
        names of all the players south east of (100, 100) and within 10 steps in
        either direction. In other words, find all players whose location is in
        the box with corners at: (100, 100) (110, 100) (100, 110) (110, 110)

        Runtime: faster than O(n) when distance is small

        === precondition ===
        direction in ['NE', 'SE', 'NE', 'SW']
        """
        raise NotImplementedError

    def size(self) -> int:
        """ Return the number of nodes in <self>

        Runtime: O(n)
        """
        raise NotImplementedError

    def height(self) -> int:
        """ Return the height of <self>

        Height is measured as the number of nodes in the path from the root of
        this tree to the node at the greatest depth in this tree.

        Runtime: O(n)
        """
        raise NotImplementedError

    def depth(self, tree: Tree) -> Optional[int]:
        """ Return the depth of the subtree <tree> relative to <self>. Return
        None if <tree> is not a descendant of <self>

        Runtime: O(log(n))
        """
        raise NotImplementedError

    def is_leaf(self) -> bool:
        """ Return True if <self> has no children. is_leaf

        Runtime: O(1)
        """
        raise NotImplementedError

    def is_empty(self) -> bool:
        """ Return True if <self> or any of its descendants do not store any
        information about the location of any players. is_empty

        Runtime: O(1)
        """
        raise NotImplementedError


class QuadTree(Tree):
    """ QuadTree is a Quad Tree that is a subclass of Tree.
    It sorts players/people into a square field where each quadrant is named
    and may have sub-quadrants.
    If there are two players in the same quadrants, we want to sort them into
    sub-quadrants of this quadrant. This means that quadrants with a name
    and point will only exist in leaves of the tree.

    === Attributes ===
    _centre : the centre of the field/quadrant
    _name : the name of a player in this quadrant (or None if there
        are sub-quadrants)
    _point : the point of the player in this quadrant (or None if there
        are sub-quadrants
    _ne : the north-eastern quadrant in this field of this centre
    _nw : the north-western quadrant in this field of this centre
    _se : the south-eastern quadrant in this field of this centre
    _sw : the south-western quadrant in this field of this centre

    === Representation Invariants ===
    If any of _ne, _nw, _se, _sw are not None, then this quadrant cannot have
        a _name or _point value.
    If all of those are None, then this can have a _name and _point value.
    If all of those are None and there are no _name or _point value then
        the tree is considered empty.

    === DocTests ===
    >>> quad = QuadTree((250, 250))
    >>> quad._ne is None
    True
    >>> quad._nw is None
    True
    >>> quad._se is None
    True
    >>> quad._sw is None
    True
    >>> quad._name is None and quad._point is None
    True
    >>> quad._centre == (250, 250)
    True
    """
    _centre: Tuple[int, int]
    _name: Optional[str]
    _point: Optional[Tuple[int, int]]
    _ne: Optional[QuadTree]
    _nw: Optional[QuadTree]
    _se: Optional[QuadTree]
    _sw: Optional[QuadTree]

    def __init__(self, centre: Tuple[int, int]) -> None:
        """Initialize a new Tree instance with a centre at self

        Runtime: O(1)

        Preconditions

        === DocTests ===
        >>> quad = QuadTree((250, 250))
        >>> quad._ne is None
        True
        >>> quad._nw is None
        True
        >>> quad._se is None
        True
        >>> quad._sw is None
        True
        >>> quad._name is None and quad._point is None
        True
        >>> quad._centre == (250,250)
        True
        """
        self._centre = centre
        self._name = None
        self._point = None
        self._ne = None
        self._nw = None
        self._se = None
        self._sw = None

    def __contains__(self, name: str) -> bool:
        """ Return True if a player named <name> is stored in this tree.
        __contains__ checks if name is contained in self
        Runtime: O(n)

        Preconditions

        === DocTests ===
        >>> quad = QuadTree((250, 250))
        >>> quad.insert('1', (250, 250))
        >>> quad.insert('2', (350, 350))
        >>> '1' in quad
        True
        >>> '2' in quad
        True
        >>> '3' in quad
        False
        """
        if self._name is not None:
            return name == self._name
        if self._nw is not None:
            if self._nw.__contains__(name):
                return True
        if self._ne is not None:
            if self._ne.__contains__(name):
                return True
        if self._sw is not None:
            if self._sw.__contains__(name):
                return True
        if self._se is not None:
            if self._se.__contains__(name):
                return True
        return False

    def contains_point(self, point: Tuple[int, int]) -> bool:
        """ Return True if a player at location <point> is stored in this tree.
        contains_point checks if point is in self
        Runtime: O(log(n))

        Preconditions

        === DocTests ===
        >>> quad = QuadTree((250, 250))
        >>> quad.insert('1', (250, 250))
        >>> quad.insert('2', (350, 350))
        >>> quad.contains_point((250, 250))
        True
        >>> quad.contains_point((350, 350))
        True
        >>> quad.contains_point((450, 450))
        False
        """
        if self.is_empty():
            return False
        elif self._point is not None:
            return self._point == point
        else:
            if point[0] <= self._centre[0] and point[1] <= self._centre[
                    1] and self._nw is not None:
                return self._nw.contains_point(point)
            elif point[0] <= self._centre[0] and self._sw is not None:
                return self._sw.contains_point(point)
            elif point[1] <= self._centre[1] and self._ne is not None:
                return self._ne.contains_point(point)
            elif point[1] > self._centre[1] and self._se is not None:
                return self._se.contains_point(point)

    def _helper_shorten_insert(self, subtree: QuadTree, name: str,
                               point: Tuple[int, int]) -> None:
        """ _helper_shorten_insert is helper shorten insert.
        It takes a subtree name and point and returns nothing in self.
        It checks if something is out of bounds then sets a new subquadrant
        and then reinserts the original point

        === Preconditions ===
        The point is not out of the field's bounds. This is already checked for
        within insert so it is no problem unless helper method run independently
        """
        if subtree._name is not None and subtree._point == point:
            raise OutOfBoundsError
        new = self._helper_create_quadrant(subtree, point)
        if new._name is None and new.is_leaf():
            new._name = name
            new._point = point
        else:
            subtree.insert(name, point)
        if subtree._name is not None:
            na, po = subtree._name, subtree._point
            subtree._name, subtree._point = None, None
            self.insert(na, po)

    def insert(self, name: str, point: Tuple[int, int]) -> None:
        """Insert a player named <name> into this tree at point <point>. insert
        insert a point and name into self
        Raise an OutOfBoundsError if <point> is out of bounds.

        Raise an OutOfBoundsError if moving the player would place the player at
        exactly the same coordinates of another player in the Tree (before
        moving the player).

        Runtime: O(log(n))

        Preconditions

        === DocTests ===
        >>> quad = QuadTree((250, 250))
        >>> quad.insert('1', (250, 250))
        >>> quad.insert('2', (350, 350))
        >>> '1' in quad
        True
        >>> '2' in quad
        True
        >>> try:
        ...     quad.insert('3', (250, 250))
        ... except OutOfBoundsError:
        ...     print('Error')
        Error
        >>> try:
        ...     quad.insert('3', (501, 501))
        ... except OutOfBoundsError:
        ...     print('Error')
        Error
        """
        better = max(self._centre[0], self._centre[1])
        if point[0] > better*2 or point[1] > better*2 or point[0] < 0 or point[
                1] < 0:
            raise OutOfBoundsError
        elif self.is_empty():
            self._name = name
            self._point = point
        elif self._point is not None and (self.is_leaf()):
            n, self._point = self._point, None
            self.insert(self._name, n)
            self._name = None
            self.insert(name, point)
        else:
            half = int(self._centre[0] / 2)
            if point[0] <= self._centre[0] and point[1] <= self._centre[1]:
                if self._nw is None:
                    self._nw = QuadTree((half, half))
                    self._nw._name = name
                    self._nw._point = point
                else:
                    self._helper_shorten_insert(self._nw, name, point)
            elif point[0] <= self._centre[0]:
                if self._sw is None:
                    self._sw = QuadTree((half, self._centre[1] + half))
                    self._sw.insert(name, point)
                else:
                    self._helper_shorten_insert(self._sw, name, point)
            elif point[1] <= self._centre[1]:
                if self._ne is None:
                    self._ne = QuadTree((self._centre[0] + half, half))
                    self._ne.insert(name, point)
                else:
                    self._helper_shorten_insert(self._ne, name, point)
            else:
                if self._se is None:
                    self._se = QuadTree(
                        (self._centre[0] + half, self._centre[1] + half))
                    self._se.insert(name, point)
                else:
                    self._helper_shorten_insert(self._se, name, point)

    def _helper_create_quadrant(self, quadrant: QuadTree,
                                point: Tuple[int, int]) -> QuadTree:
        """ _helper_create_quadrant is helper create quadrant.
        It takes a quadrant and point and returns a QuadTree in self.
        It uses the current centre and the quadrant's centre to find
        the next centre and create and return it. Preconditions
        """
        half = abs(self._centre[0] - quadrant._centre[0]) / 2
        if point[0] <= quadrant._centre[0] and point[1] <= quadrant._centre[1]:
            if quadrant._nw is None:
                quadrant._nw = QuadTree(
                    (int(quadrant._centre[0] - half),
                     quadrant._centre[1] - int(half)))
            return quadrant._nw
        elif point[0] <= quadrant._centre[0]:
            if quadrant._sw is None:
                quadrant._sw = QuadTree(
                    (quadrant._centre[0] - int(half),
                     int(quadrant._centre[1] + half)))
            return quadrant._sw
        elif point[1] <= quadrant._centre[1]:
            if quadrant._ne is None:
                quadrant._ne = QuadTree(
                    (int(quadrant._centre[0] + half),
                     quadrant._centre[1] - int(half)))
            return quadrant._ne
        else:
            if quadrant._se is None:
                quadrant._se = QuadTree(
                    (int(quadrant._centre[0] + half),
                     int(quadrant._centre[1] + half)))
            return quadrant._se

    def remove(self, name: str) -> None:
        """ Remove information about a player named <name> from this tree.
        remove a name from self
        Runtime: O(n)

        Preconditions

        === DocTests ===
        >>> quad = QuadTree((250, 250))
        >>> quad.insert('1', (250, 250))
        >>> quad.insert('2', (350, 350))
        >>> '1' in quad
        True
        >>> quad.remove('1')
        >>> '1' in quad
        False
        """
        if self.is_leaf():
            if self._name == name:
                self._name, self._point = None, None
        else:
            if self._nw is not None:
                if name in self.names_in_range(self._centre, 'NW',
                                               self._centre[0]):
                    self._nw.remove(name)
                    self._helper_remove_extra_nodes()
                    return None
            if self._sw is not None:
                if name in self.names_in_range(
                        (self._centre[0], self._centre[1] + 1), 'SW',
                        self._centre[0]):
                    self._sw.remove(name)
                    self._helper_remove_extra_nodes()
                    return None
            if self._ne is not None:
                if name in self.names_in_range(
                        (self._centre[0] + 1, self._centre[1]), 'NE',
                        self._centre[0]):
                    self._ne.remove(name)
                    self._helper_remove_extra_nodes()
                    return None
            if self._se is not None:
                if name in self.names_in_range(
                        (self._centre[0] + 1, self._centre[1] + 1), 'SE',
                        self._centre[0]):
                    self._se.remove(name)
                    self._helper_remove_extra_nodes()
                    return None

    def _helper_remove_extra_nodes(self) -> None:
        """ _helper_remove_nodes is helper remove nodes.
        It takes self and removes its extra empty leaves
        Preconditions
        """
        if self._nw is not None and self._nw.is_empty():
            self._nw = None
        if self._sw is not None and self._sw.is_empty():
            self._sw = None
        if self._ne is not None and self._ne.is_empty():
            self._ne = None
        if self._se is not None and self._se.is_empty():
            self._se = None
        if self._nw is not None and self._sw is None and self._se is None and (
                self._ne is None):
            if self._nw.is_leaf():
                self._name, self._point = self._nw._name, self._nw._point
                self._nw = None
        if self._sw is not None and self._nw is None and self._se is None and (
                self._ne is None):
            if self._sw.is_leaf():
                self._name, self._point = self._sw._name, self._sw._point
                self._sw = None
        if self._ne is not None and self._sw is None and self._se is None and (
                self._nw is None):
            if self._ne.is_leaf():
                self._name, self._point = self._ne._name, self._ne._point
                self._ne = None
        if self._se is not None and self._sw is None and self._nw is None and (
                self._ne is None):
            if self._se.is_leaf():
                self._name, self._point = self._se._name, self._se._point
                self._se = None

    def remove_point(self, point: Tuple[int, int]) -> None:
        """ Remove information about a player at point <point> from this tree.
        remove_point removes a point in self
        Runtime: O(log(n))

        Preconditions

        === DocTests ===
        >>> quad = QuadTree((250, 250))
        >>> quad.insert('1', (250, 250))
        >>> quad.insert('2', (350, 350))
        >>> '1' in quad
        True
        >>> quad.remove_point((250,250))
        >>> quad.contains_point((250,250))
        False
        """
        if self.is_leaf():
            if self._point == point:
                self._name, self._point = None, None
        elif not self.is_empty():
            if point[0] <= self._centre[0] and point[1] <= self._centre[
                    1] and self._nw is not None:
                self._nw.remove_point(point)
                self._helper_remove_extra_nodes()
            elif point[0] <= self._centre[0] and self._sw is not None:
                self._sw.remove_point(point)
                self._helper_remove_extra_nodes()
            elif point[1] <= self._centre[1] and self._ne is not None:
                self._ne.remove_point(point)
                self._helper_remove_extra_nodes()
            elif point[1] > self._centre[1] and self._se is not None:
                self._se.remove_point(point)
                self._helper_remove_extra_nodes()

    def _helper_move(self, name: str, direction: str, steps: int) -> List[
            Tuple[int, int], Tuple[int, int]]:
        """ _helper_move is helper move.
        It takes self name direction steps and returns a list of tuples.
        It returns the old point and new point

        === Preconditions ===
        direction in ['N', 'S', 'E', 'W']
        """
        if self.is_leaf() and self._name == name:
            if direction == 'N':
                points = (self._point[0], self._point[1] - steps)
                return [self._point, points]
            elif direction == 'S':
                points = (self._point[0], self._point[1] + steps)
                return [self._point, points]
            elif direction == 'W':
                points = (self._point[0] - steps, self._point[1])
                return [self._point, points]
            else:
                points = (self._point[0] + steps, self._point[1])
                return [self._point, points]
        else:
            if self._nw is not None and name in self._nw:
                return self._nw._helper_move(name, direction, steps)
            elif self._sw is not None and name in self._sw:
                return self._sw._helper_move(name, direction, steps)
            elif self._ne is not None and name in self._ne:
                return self._ne._helper_move(name, direction, steps)
            elif self._se is not None and name in self._se:
                return self._se._helper_move(name, direction, steps)

    def move(self, name: str, direction: str, steps: int) -> Optional[
            Tuple[int, int]]:
        """ Return the new location of the player named <name> after moving it
        in the given <direction> by <steps> steps.
        move a name a direction by steps in self
        Raise an OutOfBoundsError if this would move the player named
        <name> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at
        exactly the same coordinates of another player in the Tree (before
        moving the player).

        Runtime: O(n)

        === Preconditions ===
        direction in ['N', 'S', 'E', 'W']

        === DocTests ===
        >>> quad = QuadTree((250, 250))
        >>> quad.insert('1', (250, 250))
        >>> quad.insert('2', (350, 350))
        >>> '1' in quad
        True
        >>> '2' in quad
        True
        >>> quad.move('2', 'N', 100)
        (350, 250)
        >>> try:
        ...     quad.move('1', 'E', 100)
        ... except OutOfBoundsError:
        ...     print('Error')
        Error
        """
        if name in self:
            values = self._helper_move(name, direction, steps)
            self.remove_point(values[0])
            try:
                self.insert(name, values[1])
            except OutOfBoundsError:
                self.insert(name, values[0])
                raise OutOfBoundsError
            return values[1]

    def _helper_move_point(self, point: Tuple[int, int], direction: str,
                           steps: int) -> List[str, Tuple[int, int]]:
        """ _helper_move_point is helper move point.
        It takes self point direction and steps and returns a string and a
        tuple. These are the name and the new point.

        === Preconditions ===
        direction in ['N', 'S', 'E', 'W']
        """
        if self.is_leaf() and self._point == point:
            if direction == 'N':
                points = (self._point[0], self._point[1] - steps)
                return [self._name, points]
            elif direction == 'S':
                points = (self._point[0], self._point[1] + steps)
                return [self._name, points]
            elif direction == 'W':
                points = (self._point[0] - steps, self._point[1])
                return [self._name, points]
            else:
                points = (self._point[0] + steps, self._point[1])
                return [self._name, points]
        elif not self.is_empty():
            if point[0] <= self._centre[0] and point[1] <= self._centre[
                    1] and self._nw is not None:
                return self._nw._helper_move_point(point, direction, steps)
            elif point[0] <= self._centre[0] and self._sw is not None:
                return self._sw._helper_move_point(point, direction, steps)
            elif point[1] <= self._centre[1] and self._ne is not None:
                return self._ne._helper_move_point(point, direction, steps)
            elif point[1] > self._centre[1] and self._se is not None:
                return self._se._helper_move_point(point, direction, steps)

    def move_point(self, point: Tuple[int, int], direction: str, steps: int) ->\
            Optional[Tuple[int, int]]:
        """ Return the new location of the player at point <point> after moving
        it in the given <direction> by <steps> steps.
        move_point moves a point in direction by steps in self
        Raise an OutOfBoundsError if this would move the player at point
        <point> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at
        exactly the same coordinates of another player in the Tree (before
        moving the player).

        Moving a point may require the tree to be reorganized. This method
        should do the minimum amount of tree reorganization possible to move
        the given point properly.

        Runtime: O(log(n))

        === Preconditions ===
        direction in ['N', 'S', 'E', 'W']

        === DocTests ===
        >>> quad = QuadTree((250, 250))
        >>> quad.insert('1', (250, 250))
        >>> quad.insert('2', (350, 350))
        >>> '1' in quad
        True
        >>> '2' in quad
        True
        >>> quad.move_point((350,350), 'N', 100)
        (350, 250)
        >>> try:
        ...     quad.move_point((250,250), 'E', 100)
        ... except OutOfBoundsError:
        ...     print('Error')
        Error
        """
        if self.contains_point(point):
            values = self._helper_move_point(point, direction, steps)
            if values is not None and values[1] is not None:
                self.remove_point(point)
                try:
                    self.insert(values[0], values[1])
                except OutOfBoundsError:
                    self.insert(values[0], point)
                    raise OutOfBoundsError
                return values[1]

    def names_in_range(self, point: Tuple[int, int], direction: str,
                       distance: int) -> List[str]:
        """ Return a list of names of players whose location is in the
        <direction> relative to <point> and whose location is within <distance>
        along both the x and y axis.
        names_in_range searches in direction from point for distance in self
        For example: names_in_range((100, 100), 'SE', 10) should return the
        names of all the players south east of (100, 100) and within 10 steps in
        either direction. In other words, find all players whose location is in
        the box with corners at: (100, 100) (110, 100) (100, 110) (110, 110)

        Runtime: faster than O(n) when distance is small

        === Preconditions ===
        direction in ['NW', 'SE', 'NE', 'SW']

        === DocTests ===
        >>> quad = QuadTree((250, 250))
        >>> quad.insert('1', (250, 250))
        >>> quad.insert('2', (350, 350))
        >>> quad.names_in_range((500,500), 'NW', 500)
        ['1', '2']
        """
        if direction == 'NW':
            other = (point[0] - distance, point[1] - distance)
        elif direction == 'SW':
            other = (point[0] - distance, point[1] + distance)
        elif direction == 'SE':
            other = (point[0] + distance, point[1] + distance)
        elif direction == 'NE':
            other = (point[0] + distance, point[1] - distance)
        xmin = min(point[0], other[0])
        xmas = max(point[0], other[0])
        ymin = min(point[1], other[1])
        ymax = max(point[1], other[1])
        if self.is_leaf():
            if not self.is_empty() and (xmin <= self._point[0] <= xmas) and (
                    ymin <= self._point[1] <= ymax):
                return [self._name]
            return []
        else:
            result = []
            if self._nw is not None:
                result += self._nw.names_in_range(point, direction, distance)
            if self._sw is not None:
                result += self._sw.names_in_range(point, direction, distance)
            if self._ne is not None:
                result += self._ne.names_in_range(point, direction, distance)
            if self._se is not None:
                result += self._se.names_in_range(point, direction, distance)
            return result

    def size(self) -> int:
        """ Return the number of nodes in <self>

        Runtime: O(n)

        Preconditions

        === DocTests ===
        >>> quad = QuadTree((250, 250))
        >>> quad.insert('1', (250, 250))
        >>> quad.insert('2', (350, 350))
        >>> quad.size()
        3
        """
        if self.is_empty() or self.is_leaf():
            return 1
        else:
            count = 1
            if self._nw is not None:
                count += self._nw.size()
            if self._sw is not None:
                count += self._sw.size()
            if self._ne is not None:
                count += self._ne.size()
            if self._se is not None:
                count += self._se.size()
            return count

    def height(self) -> int:
        """ Return the height of <self>

        Height is measured as the number of nodes in the path from the root of
        this tree to the node at the greatest depth in this tree.

        Runtime: O(n)

        Preconditions

        === DocTests ===
        >>> quad = QuadTree((250, 250))
        >>> quad.insert('1', (250, 250))
        >>> quad.insert('2', (350, 350))
        >>> quad.height()
        2
        """
        if self.is_empty() or self.is_leaf():
            return 1
        else:
            height = 1
            nw_h = 0
            ne_h = 0
            sw_h = 0
            se_h = 0
            if self._nw is not None:
                nw_h = self._nw.height()
            if self._sw is not None:
                sw_h = self._sw.height()
            if self._ne is not None:
                ne_h = self._ne.height()
            if self._se is not None:
                se_h = self._se.height()
            height += max(nw_h, sw_h, ne_h, se_h)
            return height

    def depth(self, tree: QuadTree) -> Optional[int]:
        """ Return the depth of the subtree <tree> relative to <self>. Return
        None if <tree> is not a descendant of <self>

        Runtime: O(log(n))

        Preconditions

        === DocTests ===
        >>> quad = QuadTree((250, 250))
        >>> quad.insert('1', (250, 250))
        >>> quad.insert('2', (350, 350))
        >>> quad.depth(quad._nw)
        1
        >>> t = QuadTree((50,50))
        >>> quad.depth(t)
        """
        if self.is_leaf() or self.is_empty() or tree is None:
            return None
        else:
            count = 0
            if tree._centre[0] < self._centre[0] and tree._centre[1] < \
                    self._centre[1]:
                if self._nw is tree:
                    return 1
                elif self._nw.depth(tree) is None:
                    return None
                count = 1
                count += self._nw.depth(tree)
            elif tree._centre[0] < self._centre[0] and tree._centre[1] < \
                    self._centre[1]:
                if self._sw is tree:
                    return 1
                elif self._sw.depth(tree) is None:
                    return None
                count = 1
                count += self._sw.depth(tree)
            elif tree._centre[1] < self._centre[1] and tree._centre[0] > \
                    self._centre[0]:
                if self._ne is tree:
                    return 1
                elif self._ne.depth(tree) is None:
                    return None
                count = 1
                count += self._ne.depth(tree)
            elif tree._centre[0] > self._centre[0] and tree._centre[1] > \
                    self._centre[1]:
                if self._se is tree:
                    return 1
                elif self._se.depth(tree) is None:
                    return None
                count = 1
                count += self._se.depth(tree)
            if count == 0:
                return None
            return count

    def is_leaf(self) -> bool:
        """ Return True if <self> has no children is_leaf

        Runtime: O(1)
        Preconditions

        === DocTests ===
        >>> quad = QuadTree((250, 250))
        >>> quad.insert('1', (250, 250))
        >>> quad.insert('2', (350, 350))
        >>> quad.is_leaf()
        False
        >>> quad._nw.is_leaf()
        True
        """
        return self._nw is None and self._ne is None and self._sw is None and (
            self._se is None)

    def is_empty(self) -> bool:
        """ Return True if <self> or any of its descendants do not store any
        information about the location of any players. is_empty

        Runtime: O(1)
        Preconditions

        === DocTests ===
        >>> quad = QuadTree((250, 250))
        >>> quad.is_empty()
        True
        >>> quad.insert('1', (250, 250))
        >>> quad.insert('2', (350, 350))
        >>> quad.is_empty()
        False
        """
        return self._name is None and self._point is None and (
            self._nw is None) and self._ne is None and (
                self._sw is None) and self._se is None


class TwoDTree(Tree):
    """ TwoDTree is a Two D Tree that is a subclass of Tree.
    It sorts players/people into a field where each node has a name and point
    value.
    After the first player is inserted, each following player is either
    placed in the less than or greater than subtree which alternates between
    sorting along the y-axis and x-axis.
    This means that no node should ever be empty (without name and point)
    apart from its initialization.

    === Attributes ===
    _name : the name of a player in this tree/node
    _point : the point of the player in this tree/node
    _ne : the north-eastern corner of this tree
        This is None if it is not the root node
    _se : the south-eastern corner of this tree
        This is None if it is not the root node
    _lt : the tree with nodes less than or equal to the current position in
        either the y or x axis of this current point
    _gt : the tree with nodes greater than the current position in either
        the y or x axis of this current point
    _split_type : the split type of this tree, either along the x axis or y axis

    === Representation Invariants ===
    If _nw, _se are not None, then this tree is not the root value.
        Otherwise, it is the root of the tree.
    Unless upon initialization of the tree, _name and _point must not be None.
    _split_type is either 'x' or 'y'.
    _nw must have values less than _se

    === DocTests ===
        >>> two = TwoDTree((0, 0), (500, 500))
        >>> two._nw == (0, 0)
        True
        >>> two._se == (500, 500)
        True
        >>> two._name is None and two._point is None
        True
        >>> two._lt is None and two._gt is None
        True
        >>> two._split_type == 'x'
        True
    """
    _name: Optional[str]
    _point: Optional[Tuple[int, int]]
    _nw: Optional[Tuple[int, int]]
    _se: Optional[Tuple[int, int]]
    _lt: Optional[TwoDTree]
    _gt: Optional[TwoDTree]
    _split_type: str

    def __init__(self, nw: Optional[Tuple[int, int]],
                 se: Optional[Tuple[int, int]]) -> None:
        """Initialize a new Tree instance in self with nw and se corners.

        Runtime: O(1)

        === Preconditions ===
        nw[0] < se[0] and sw[1] < se[1]

        === DocTests ===
        >>> two = TwoDTree((0, 0), (500, 500))
        >>> two._nw == (0, 0)
        True
        >>> two._se == (500, 500)
        True
        >>> two._name is None and two._point is None
        True
        >>> two._lt is None and two._gt is None
        True
        >>> two._split_type == 'x'
        True
        """
        self._name = None
        self._point = None
        self._nw = nw
        self._se = se
        self._lt = None
        self._gt = None
        self._split_type = 'x'

    def __contains__(self, name: str) -> bool:
        """ Return True if a player named <name> is stored in this tree.
        __contains__ checks if name is contained in self
        Runtime: O(n)

        Preconditions

        === DocTests ===
        >>> two = TwoDTree((0, 0), (500, 500))
        >>> two.insert('1', (250, 250))
        >>> two.insert('2', (350, 350))
        >>> '1' in two
        True
        >>> '2' in two
        True
        >>> '3' in two
        False
        """
        if self._name == name:
            return True
        elif self.is_leaf() or self.is_empty():
            return False
        else:
            indicator_g = False
            indicator_l = False
            if self._lt is not None:
                indicator_l = name in self._lt
            if self._gt is not None:
                indicator_g = name in self._gt
            return indicator_g or indicator_l

    def contains_point(self, point: Tuple[int, int]) -> bool:
        """ Return True if a player at location <point> is stored in this tree.
        contains_point checks if point is in self
        Runtime: O(log(n))

        === Preconditions ===
        nw[0] < se[0] and sw[1] < se[1]

        === DocTests ===
        >>> two = TwoDTree((0, 0), (500, 500))
        >>> two.insert('1', (250, 250))
        >>> two.insert('2', (350, 350))
        >>> two.contains_point((250, 250))
        True
        >>> two.contains_point((350, 350))
        True
        >>> two.contains_point((450, 450))
        False
        """
        if self._point == point:
            return True
        elif self._point is None or self._name is None or (
                self._lt is None and self._gt is None):
            return False
        elif self._split_type == 'x':
            if point[0] <= self._point[0] and self._lt is not None:
                return self._lt.contains_point(point)
            elif self._gt is not None:
                return self._gt.contains_point(point)
            return False
        elif self._split_type == 'y':
            if point[1] <= self._point[1] and self._lt is not None:
                return self._lt.contains_point(point)
            elif self._gt is not None:
                return self._gt.contains_point(point)
            return False

    def insert(self, name: str, point: Tuple[int, int]) -> None:
        """Insert a player named <name> into this tree at point <point>.
        insert a point and a name into self
        Raise an OutOfBoundsError if <point> is out of bounds.

        Raise an OutOfBoundsError if moving the player would place the player at
        exactly the same coordinates of another player in the Tree (before
        moving the player).

        Runtime: O(log(n))

        Preconditions

        === DocTests ===
        >>> two = TwoDTree((0, 0), (500, 500))
        >>> two.insert('1', (250, 250))
        >>> two.insert('2', (350, 350))
        >>> '1' in two
        True
        >>> '2' in two
        True
        >>> try:
        ...     two.insert('3', (250, 250))
        ... except OutOfBoundsError:
        ...     print('Error')
        Error
        >>> try:
        ...     two.insert('3', (501, 501))
        ... except OutOfBoundsError:
        ...     print('Error')
        Error
        """
        if self._point == point:
            raise OutOfBoundsError
        elif self._nw is not None and self._se is not None and (
                point[0] < self._nw[0] or point[0] > self._se[0] or point[1] <
                self._nw[1] or point[1] > self._se[1]):
            raise OutOfBoundsError
        elif self.is_empty():
            self._name = name
            self._point = point
        elif self._point is not None:
            if self._split_type == 'x':
                if point[0] <= self._point[0]:
                    if self._lt is None:
                        self._lt = TwoDTree(None, None)
                        self._lt._split_type = 'y'
                    self._lt.insert(name, point)
                else:
                    if self._gt is None:
                        self._gt = TwoDTree(None, None)
                        self._gt._split_type = 'y'
                    self._gt.insert(name, point)
            else:
                if point[1] <= self._point[1]:
                    if self._lt is None:
                        self._lt = TwoDTree(None, None)
                        self._lt._split_type = 'x'
                    self._lt.insert(name, point)
                else:
                    if self._gt is None:
                        self._gt = TwoDTree(None, None)
                        self._gt._split_type = 'x'
                    self._gt.insert(name, point)

    def _helper_remove_empty_leaves(self) -> None:
        """ _helper_remove_empty_leaves is helper remove empty leaves.
        It takes self and removes its empty leaves.
        Preconditions
        """
        if self._lt is not None:
            if self._lt.is_leaf() and self._lt.is_empty():
                self._lt = None
            else:
                self._lt._helper_remove_empty_leaves()
        if self._gt is not None:
            if self._gt.is_empty() and self._gt.is_leaf():
                self._gt = None
            else:
                self._gt._helper_remove_empty_leaves()

    def _helper_get_descendants(self) -> List[Tuple[str, Tuple[int, int]]]:
        """ _helper_get_descendants is helper get descendants.
        It takes self and reutrns all of its descendants as a list of tuples
        containing their name and location.
        Preconditions
        """
        results = [(self._name, self._point)]
        if self._lt is not None:
            results += self._lt._helper_get_descendants()
        if self._gt is not None:
            results += self._gt._helper_get_descendants()
        return results

    def remove(self, name: str) -> None:
        """ Remove information about a player named <name> from this tree.
        remove a name from self
        Runtime: O(n)

        Preconditions

        === DocTests ===
        >>> two = TwoDTree((0, 0), (500, 500))
        >>> two.insert('1', (250, 250))
        >>> two.insert('2', (350, 350))
        >>> '1' in two
        True
        >>> '2' in two
        True
        >>> two.remove('1')
        >>> '1' in two
        False
        """
        if self._name == name:
            self._name = None
            self._point = None
            if not self.is_leaf():
                descendants = self._helper_get_descendants()
                self._lt = None
                self._gt = None
                for person in descendants:
                    if person[0] is not None and person[1] is not None:
                        self.insert(person[0], person[1])
        else:
            if self._lt is not None and name in self._lt:
                self._lt.remove(name)
            elif self._gt is not None and name in self._gt:
                self._gt.remove(name)

    def remove_point(self, point: Tuple[int, int]) -> None:
        """ Remove information about a player at point <point> from this tree.
        remove_point removes a point in self
        Runtime: O(log(n))

        Preconditions

        === DocTests ===
        >>> two = TwoDTree((0, 0), (500, 500))
        >>> two.insert('1', (250, 250))
        >>> two.insert('2', (350, 350))
        >>> '1' in two
        True
        >>> '2' in two
        True
        >>> two.remove_point((250, 250))
        >>> two.contains_point((250, 250))
        False
        """
        if self._point == point:
            self._name = None
            pt = self._point
            self._point = None
            if not self.is_leaf():
                if self._lt is not None:
                    replace = self._lt._helper_closest(pt, self._split_type)
                    if replace is not None:
                        replace_name = replace._name
                        replace_pt = replace._point
                        self._lt.remove_point(replace._point)
                        self._name = replace_name
                        self._point = replace_pt
                else:
                    replace = self._gt._helper_closest(pt, self._split_type)
                    if replace is not None:
                        replace_name = replace._name
                        replace_pt = replace._point
                        self._gt.remove_point(replace._point)
                        self._name = replace_name
                        self._point = replace_pt
            self._helper_remove_empty_leaves()
        elif self._point is not None and not self.is_empty():
            if self._split_type == 'x':
                if point[0] <= self._point[0]:
                    if self._lt is not None:
                        self._lt.remove_point(point)
                else:
                    if self._gt is not None:
                        self._gt.remove_point(point)
            else:
                if point[1] <= self._point[1]:
                    if self._lt is not None:
                        self._lt.remove_point(point)
                else:
                    if self._gt is not None:
                        self._gt.remove_point(point)

    def _helper_move(self, name: str, direction: str, steps: int) -> List[
            Tuple[int, int], Tuple[int, int]]:
        """ _helper_move is helper move.
        It takes self name direction and steps and returns a list of tuples.
        It returns the old location and new location of the point.

        === Preconditions ===
        direction in ['N', 'S', 'E', 'W']
        """
        if self._name == name:
            if direction == 'N':
                points = (self._point[0], self._point[1] - steps)
                return [self._point, points]
            elif direction == 'S':
                points = (self._point[0], self._point[1] + steps)
                return [self._point, points]
            elif direction == 'W':
                points = (self._point[0] - steps, self._point[1])
                return [self._point, points]
            else:
                points = (self._point[0] + steps, self._point[1])
                return [self._point, points]
        else:
            if self._lt is not None and name in self._lt:
                return self._lt._helper_move(name, direction, steps)
            elif self._gt is not None and name in self._gt:
                return self._gt._helper_move(name, direction, steps)

    def move(self, name: str, direction: str, steps: int) -> Optional[
            Tuple[int, int]]:
        """ Return the new location of the player named <name> after moving it
        in the given <direction> by <steps> steps.
        move name a direction for steps in self
        Raise an OutOfBoundsError if this would move the player named
        <name> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at
        exactly the same coordinates of another player in the Tree (before
        moving the player).

        Runtime: O(n)

        === Preconditions ===
        direction in ['N', 'S', 'E', 'W']

        === DocTests ===
        >>> two = TwoDTree((0, 0), (500, 500))
        >>> two.insert('1', (250, 250))
        >>> two.insert('2', (350, 350))
        >>> two.move('2', 'N', 100)
        (350, 250)
        >>> try:
        ...     two.move('1', 'E', 100)
        ... except OutOfBoundsError:
        ...     print('Error')
        Error
        """
        if name in self:
            values = self._helper_move(name, direction, steps)
            self.insert(name, values[1])
            self.remove_point(values[0])
            return values[1]

    def _helper_move_point(self, point: Tuple[int, int], direction: str,
                           steps: int) -> List[str, Tuple[int, int]]:
        """ _helper_move_point is helper move point.
        It takes self point direction and steps and returns a list of
        names to points.

        === Preconditions ===
        direction in ['N', 'S', 'E', 'W']
        """
        if self._point == point:
            if direction == 'N':
                points = (self._point[0], self._point[1] - steps)
                return [self._name, points]
            elif direction == 'S':
                points = (self._point[0], self._point[1] + steps)
                return [self._name, points]
            elif direction == 'W':
                points = (self._point[0] - steps, self._point[1])
                return [self._name, points]
            else:
                points = (self._point[0] + steps, self._point[1])
                return [self._name, points]
        elif self._point is not None:
            if self._split_type == 'x' and point[0] <= self._point[
                    0] and self._lt is not None:
                return self._lt._helper_move_point(point, direction, steps)
            elif self._split_type == 'x' and point[0] > self._point[
                    0] and self._gt is not None:
                return self._gt._helper_move_point(point, direction, steps)
            elif self._split_type == 'y' and point[1] <= self._point[
                    1] and self._lt is not None:
                return self._lt._helper_move_point(point, direction, steps)
            elif self._split_type == 'y' and point[1] > self._point[
                    1] and self._gt is not None:
                return self._gt._helper_move_point(point, direction, steps)

    def move_point(self, point: Tuple[int, int], direction: str, steps: int) ->\
            Optional[Tuple[int, int]]:
        """ Return the new location of the player at point <point> after moving
        it in the given <direction> by <steps> steps.
        move_point moves a point a direction for steps in self
        Raise an OutOfBoundsError if this would move the player at point
        <point> out of bounds (before moving the player).

        Raise an OutOfBoundsError if moving the player would place the player at
        exactly the same coordinates of another player in the Tree (before
        moving the player).

        Moving a point may require the tree to be reorganized. This method
        should do the minimum amount of tree reorganization possible to move the
        given point properly.

        Runtime: O(log(n))

        === Preconditions ===
        direction in ['N', 'S', 'E', 'W']

        === DocTests ===
        >>> two = TwoDTree((0, 0), (500, 500))
        >>> two.insert('1', (250, 250))
        >>> two.insert('2', (350, 350))
        >>> two.move_point((350, 350), 'N', 100)
        (350, 250)
        >>> try:
        ...     two.move_point((250, 250), 'E', 100)
        ... except OutOfBoundsError:
        ...     print('Error')
        Error
        """
        values = self._helper_move_point(point, direction, steps)
        if values is not None:
            self.insert(values[0], values[1])
            self.remove_point(point)
            return values[1]

    def names_in_range(self, point: Tuple[int, int], direction: str,
                       distance: int) -> List[str]:
        """ Return a list of names of players whose location is in the
        <direction> relative to <point> and whose location is within <distance>
        along both the x and y axis.
        names_in_range uses a point and searches in a direction for a certain
        distance in self
        For example: names_in_range((100, 100), 'SE', 10) should return the
        names of all the players south east of (100, 100) and within 10 steps in
        either direction. In other words, find all players whose location is in
        the box with corners at: (100, 100) (110, 100) (100, 110) (110, 110)

        Runtime: faster than O(n) when distance is small

        === Preconditions ===
        direction in ['NE', 'SE', 'NE', 'SW']

        === DocTests ===
        >>> two = TwoDTree((0, 0), (500, 500))
        >>> two.insert('1', (250, 250))
        >>> two.insert('2', (350, 350))
        >>> two.names_in_range((500,500), 'NW', 500)
        ['1', '2']
        """
        if direction == 'NW':
            other = (point[0] - distance, point[1] - distance)
        elif direction == 'SW':
            other = (point[0] - distance, point[1] + distance)
        elif direction == 'SE':
            other = (point[0] + distance, point[1] + distance)
        elif direction == 'NE':
            other = (point[0] + distance, point[1] - distance)
        result = []
        if self._point is not None:
            if min(other[0], point[0]) <= self._point[0] <= max(other[0], point[
                    0]) and min(other[1], point[1]) <= self._point[1] <= max(
                        other[1], point[1]):
                result = [self._name]
            if self._lt is not None:
                result += self._lt.names_in_range(point, direction, distance)
            if self._gt is not None:
                result += self._gt.names_in_range(point, direction, distance)
        return result

    def size(self) -> int:
        """ Return the number of nodes in <self>

        Runtime: O(n)

        Preconditions

        === DocTests ===
        >>> two = TwoDTree((0, 0), (500, 500))
        >>> two.insert('1', (250, 250))
        >>> two.insert('2', (350, 350))
        >>> two.size()
        2
        """
        if self.is_empty() or self.is_leaf():
            return 1
        else:
            count = 1
            if self._gt is not None:
                count += self._gt.size()
            if self._lt is not None:
                count += self._lt.size()
            return count

    def height(self) -> int:
        """ Return the height of <self>

        Height is measured as the number of nodes in the path from the root of
        this tree to the node at the greatest depth in this tree.

        Runtime: O(n)

        Preconditions

        === DocTests ===
        >>> two = TwoDTree((0, 0), (500, 500))
        >>> two.insert('1', (250, 250))
        >>> two.insert('2', (350, 350))
        >>> two.height()
        2
        """
        if self.is_empty() or self.is_leaf():
            return 1
        else:
            height = 1
            gt_h = 0
            lt_h = 0
            if self._gt is not None:
                gt_h = self._gt.height()
            if self._lt is not None:
                lt_h = self._lt.height()
            height += max(gt_h, lt_h)
            return height

    def depth(self, tree: TwoDTree) -> Optional[int]:
        """ Return the depth of the subtree <tree> relative to <self>. Return
        None if <tree> is not a descendant of <self>

        Preconditions

        Runtime: O(log(n))
        === DocTests ===
        >>> two = TwoDTree((0, 0), (500, 500))
        >>> two.insert('1', (250, 250))
        >>> two.insert('2', (350, 350))
        >>> one = TwoDTree((0, 0), (250, 250))
        >>> two.depth(one)
        >>> two.depth(two._gt)
        1
        """
        count = 0
        if tree.is_empty():
            count = 0
        elif self._split_type == 'x':
            if tree._point[0] <= self._point[0] and self._lt is not None:
                if self._lt is tree:
                    return 1
                elif self._lt.depth(tree) is not None:
                    count = 1
                    count += self._lt.depth(tree)
            elif tree._point[0] > self._point[0] and self._gt is not None:
                if self._gt is tree:
                    return 1
                elif self._gt.depth(tree) is not None:
                    count = 1
                    count += self._gt.depth(tree)
        else:
            if tree._point[1] <= self._point[1] and self._lt is not None:
                if self._lt is tree:
                    return 1
                elif self._lt.depth(tree) is not None:
                    count = 1
                    count += self._lt.depth(tree)
            elif tree._point[1] > self._point[1] and self._gt is not None:
                if self._gt is tree:
                    return 1
                elif self._gt.depth(tree) is not None:
                    count = 1
                    count += self._gt.depth(tree)
        if count == 0:
            return None
        return count

    def is_leaf(self) -> bool:
        """ Return True if <self> has no children is_leaf

        Runtime: O(1)

        Preconditions

        === DocTests ===
        >>> two = TwoDTree((0, 0), (500, 500))
        >>> two.insert('1', (250, 250))
        >>> two.insert('2', (350, 350))
        >>> two._gt.is_leaf()
        True
        >>> two.is_leaf()
        False
        """
        return self._lt is None and self._gt is None

    def is_empty(self) -> bool:
        """ Return True if <self> or any of its descendants do not store any
        information about the location of any players. is_empty

        Runtime: O(1)

        Preconditions

        === DocTests ===
        >>> two = TwoDTree((0, 0), (500, 500))
        >>> two.insert('1', (250, 250))
        >>> two.insert('2', (350, 350))
        >>> two.is_empty()
        False
        """
        return self._name is None and self._point is None and (
            self._lt is None) and self._gt is None

    def _helper_closest(self, point: Tuple[int, int], split: str) -> TwoDTree:
        """ _helper_closest is helper closest.
        It takes self point and split which is split type and returns a tree.
        This tree is the closest value to self.

        === Preconditions ===
        split in ['x', 'y']
        """
        lt_v = None
        gt_v = None
        if self._lt is not None:
            lt_v = self._lt._helper_closest(point, split)
        if self._gt is not None:
            gt_v = self._gt._helper_closest(point, split)
        if self.is_empty() or self._point is None:
            return None
        elif split == 'x':
            if lt_v is None and gt_v is None:
                return self
            elif lt_v is None:
                if abs(gt_v._point[0] - point[0]) <= abs(
                        self._point[0] - point[0]):
                    return gt_v
                else:
                    return self
            elif gt_v is None:
                if abs(lt_v._point[0] - point[0]) <= abs(
                        self._point[0] - point[0]):
                    return lt_v
                else:
                    return self
            else:
                if abs(lt_v._point[0] - point[0]) <= abs(
                        self._point[0] - point[0]) and abs(
                            lt_v._point[0] - point[0]) <= abs(
                                gt_v._point[0] - point[0]):
                    return lt_v
                elif abs(gt_v._point[0] - point[0]) <= abs(
                        self._point[0] - point[0]) and abs(
                            gt_v._point[0] - point[0]) <= abs(
                                lt_v._point[0] - point[0]):
                    return gt_v
                else:
                    return self
        else:
            if lt_v is None and gt_v is None:
                return self
            elif lt_v is None:
                if abs(gt_v._point[1] - point[1]) <= abs(
                        self._point[1] - point[1]):
                    return gt_v
                else:
                    return self
            elif gt_v is None:
                if abs(lt_v._point[1] - point[1]) <= abs(
                        self._point[1] - point[1]):
                    return lt_v
                else:
                    return self
            else:
                if abs(lt_v._point[1] - point[1]) <= abs(
                        self._point[1] - point[1]) and abs(
                            lt_v._point[1] - point[1]) <= abs(
                                gt_v._point[1] - point[1]):
                    return lt_v
                elif abs(gt_v._point[1] - point[1]) <= abs(
                        self._point[1] - point[1]) and abs(
                            gt_v._point[1] - point[1]) <= abs(
                                lt_v._point[1] - point[1]):
                    return gt_v
                else:
                    return self

    def balance(self) -> None:
        """ Balance <self> so that there is at most a difference of 1 between
        the size of the _lt subtree and the size of the _gt subtree for all
        trees in <self>. balance

        === Preconditions ===
        It is possible to balance this tree

        === DocTests ===
        >>> two = TwoDTree((0, 0), (500, 500))
        >>> two.insert('1', (250, 250))
        >>> two.insert('2', (350, 350))
        >>> two.insert('3', (300, 300))
        >>> two._lt is None
        True
        >>> two.balance()
        >>> two._lt is None
        False
        """
        if not (self._lt is None and self._gt is None):
            if self._lt is None and self._gt is not None:
                if not self._gt.is_leaf():
                    name, point = self._name, self._point
                    node = self._gt._helper_closest(point, self._split_type)
                    self._name, self._point = node._name, node._point
                    self._gt.remove_point(self._point)
                    self.insert(name, point)
                    self.balance()
            elif self._gt is None and self._lt is not None:
                if not self._lt.is_leaf():
                    name, point = self._name, self._point
                    node = self._lt._helper_closest(point, self._split_type)
                    self._name, self._point = node._name, node._point
                    self._lt.remove_point(self._point)
                    self.insert(name, point)
                    self.balance()
            elif (self._lt.size() - self._gt.size()) > 1:
                name, point = self._name, self._point
                if self._lt.size() > self._gt.size():
                    node = self._lt._helper_closest(point, self._split_type)
                    self._name, self._point = node._name, node._point
                    self._lt.remove_point(self._point)
                elif self._gt.size() > self._lt.size():
                    node = self._gt._helper_closest(point, self._split_type)
                    self._name, self._point = node._name, node._point
                    self._gt.remove_point(self._point)
                self.insert(name, point)
                self.balance()
            else:
                self._lt.balance()
                self._gt.balance()


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={'extra-imports': ['typing'],
                                'disable': ['R0913', 'R0902', 'W0611', 'R1710',
                                            'R1702']})
