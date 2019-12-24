

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
        if self._point is not None:
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

    def _helper_set_name_1(self):
        if not self._nw.is_leaf:
            self._nw._name = 1
        if not self._sw .is_leaf:
            self._sw._name = 1
        if not self._se.is_leaf:
            self._se._name = 1
        if not self._ne.is_leaf:
            self._ne._name = 1

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
        if self._name is None and (point[0] > self._centre[0] or point[1] > self._centre[1] or point[0] < 0 or point[1] < 0):  ######
            raise OutOfBoundsError
        elif self.is_empty() and self._name is None:
            self._name = name
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
        self._helper_set_name_1()

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
                     int(quadrant._centre[1] - half)))
            return quadrant._nw
        elif point[0] <= quadrant._centre[0]:
            if quadrant._sw is None:
                quadrant._sw = QuadTree(
                    (int(quadrant._centre[0] - half),
                     int(quadrant._centre[1] + half)))
            return quadrant._sw
        elif point[1] <= quadrant._centre[1]:
            if quadrant._ne is None:
                quadrant._ne = QuadTree(
                    (int(quadrant._centre[0] + half),
                     int(quadrant._centre[1] - half)))
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
                self._name, self._point = 1, None
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
                self._name, self._point = 1, None
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
        return self._point is None and (
            self._nw is None) and self._ne is None and (
                self._sw is None) and self._se is None

