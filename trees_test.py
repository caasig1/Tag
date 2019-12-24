import pytest
import trees



class TreesTest:
    def test_contains(self):
        self.tree.insert('jon', (250, 250))
        self.tree.insert('0', (500, 500))
        self.tree.insert('1', (449, 449))
        self.tree.insert('2', (448, 449))
        assert 'jon' in self.tree
        assert '0' in self.tree
        assert '1' in self.tree
        assert '2' in self.tree
        assert 'joe' not in self.tree
        assert '3' not in self.tree

    def test_tree_contains_point(self):
        self.tree.insert('jon', (250, 250))
        self.tree.insert('0', (500, 500))
        self.tree.insert('1', (449, 449))
        self.tree.insert('2', (448, 449))
        assert self.tree.contains_point((250, 250))
        assert self.tree.contains_point((500, 500))
        assert self.tree.contains_point((449, 449))
        assert self.tree.contains_point((448, 449))
        assert not self.tree.contains_point((250, 251))
        assert not self.tree.contains_point((448, 448))

    def test_insert_out_of_bounds(self):
        try:
            self.tree.insert('jon', (501, 250))
            self.tree.insert('0', (1, 501))
            self.tree.insert('1', (501, 501))
        except trees.OutOfBoundsError:
            return
        raise Exception('this should have raised an OutOfBoundsError')

    def test_insert_collision(self):
        self.tree.insert('jon', (250, 250))
        self.tree.insert('0', (400, 400))
        try:
            self.tree.insert('joe', (250, 250))
            self.tree.insert('1', (400, 400))
        except trees.OutOfBoundsError:
            return
        raise Exception('this should have raised an OutOfBoundsError')

    def test_remove(self):
        self.tree.insert('jon', (250, 250))
        self.tree.insert('0', (500, 500))
        self.tree.insert('1', (449, 449))
        self.tree.insert('2', (448, 449))
        self.tree.remove('buddy')
        self.tree.remove('3')
        assert 'jon' in self.tree
        assert '0' in self.tree
        assert '1' in self.tree
        assert '2' in self.tree
        self.tree.remove('jon')
        self.tree.remove('2')
        assert 'jon' not in self.tree
        assert '2' not in self.tree
        assert '0' in self.tree
        assert '1' in self.tree

    def test_remove_point(self):
        self.tree.insert('jon', (250, 250))
        self.tree.insert('0', (500, 500))
        self.tree.insert('1', (449, 449))
        self.tree.insert('2', (448, 449))
        self.tree.remove_point((250, 251))
        self.tree.remove_point((448, 448))
        assert 'jon' in self.tree
        assert '0' in self.tree
        assert '1' in self.tree
        assert '2' in self.tree
        self.tree.remove_point((250, 250))
        self.tree.remove_point((449, 449))
        assert 'jon' not in self.tree
        assert '1' not in self.tree
        assert '0' in self.tree
        assert '2' in self.tree

    def test_move(self):
        self.tree.insert('jon', (250, 250))
        self.tree.insert('0', (500, 500))
        self.tree.insert('1', (449, 449))
        self.tree.insert('2', (448, 449))
        self.tree.move('jon', 'N', 10)
        self.tree.move('0', 'N', 10)
        self.tree.move('1', 'W', 20)
        self.tree.move('2', 'S', 1)
        assert self.tree.contains_point((250, 240))
        assert self.tree.contains_point((500, 490))
        assert self.tree.contains_point((429, 449))
        assert self.tree.contains_point((448, 450))

    def test_move_collision(self):
        self.tree.insert('jon', (250, 250))
        self.tree.insert('joe', (250, 240))
        self.tree.insert('0', (500, 500))
        self.tree.insert('1', (449, 449))
        try:
            self.tree.move('jon', 'N', 10)
            self.tree.move('0', 'W', 1)
        except trees.OutOfBoundsError:
            return
        raise Exception('this should have raised an OutOfBoundsError')

    def test_move_out_of_bounds(self):
        self.tree.insert('jon', (250, 250))
        self.tree.insert('0', (500, 500))
        try:
            self.tree.move('jon', 'E', 251)
            self.tree.move('0', 'S', 3)
        except trees.OutOfBoundsError:
            return
        raise Exception('this should have raised an OutOfBoundsError')

    def test_move_point(self):
        self.tree.insert('jon', (250, 250))
        self.tree.insert('0', (500, 500))
        self.tree.insert('1', (449, 449))
        self.tree.insert('2', (448, 449))
        self.tree.move_point((250, 250), 'N', 10)
        self.tree.move_point((500, 500), 'N', 30)
        self.tree.move_point((449, 449), 'S', 1)
        self.tree.move_point((448, 449), 'W', 53)
        assert self.tree.contains_point((250, 240))
        assert self.tree.contains_point((500, 470))
        assert self.tree.contains_point((449, 450))
        assert self.tree.contains_point((395, 449))

    def test_move_point_collision(self):
        self.tree.insert('jon', (250, 250))
        self.tree.insert('joe', (250, 240))
        self.tree.insert('0', (0, 0))
        self.tree.insert('1', (5, 0))
        try:
            self.tree.move_point((250, 250), 'N', 10)
            self.tree.move_point((0, 0), 'S', 5)
        except trees.OutOfBoundsError:
            return
        raise Exception('this should have raised an OutOfBoundsError')

    def test_move_point_out_of_bounds(self):
        self.tree.insert('jon', (250, 250))
        self.tree.insert('0', (500, 500))
        self.tree.insert('1', (449, 449))
        try:
            self.tree.move_point((250, 250), 'E', 251)
            self.tree.move_point((500, 500), 'S', 5)
            self.tree.move_point((449, 449), 'E', 2)
        except trees.OutOfBoundsError:
            return
        raise Exception('this should have raised an OutOfBoundsError')

    def test_names_in_range(self):
        self.tree.insert('jon', (250, 250))
        self.tree.insert('joe', (300, 300))
        self.tree.insert('0', (500, 500))
        self.tree.insert('1', (449, 449))
        self.tree.insert('2', (448, 449))
        assert set(self.tree.names_in_range((200, 200), 'SE', 150)) == {'jon', 'joe'}
        assert set(self.tree.names_in_range((350, 350), 'NW', 150)) == {'jon', 'joe'}
        assert set(self.tree.names_in_range((200, 200), 'SE', 90)) == {'jon'}
        assert set(self.tree.names_in_range((350, 350), 'NW', 90)) == {'joe'}
        assert len(self.tree.names_in_range((350, 350), 'NW', 10)) == 0
        assert set(self.tree.names_in_range((400, 400), 'SE', 99)) == {'1', '2'}
        assert set(self.tree.names_in_range((0, 500), 'NE', 500)) == {'joe', 'jon', '0', '1', '2'}
        assert len(self.tree.names_in_range((448, 448), 'SE', 1)) == 2

    def test_is_empty(self):
        assert self.tree.is_empty()
        self.tree.insert('jon', (250, 250))
        self.tree.remove('jon')
        self.tree.insert('0', (500, 500))
        assert not self.tree.is_empty()

    def test_is_leaf(self):
        assert self.tree.is_leaf()
        self.tree.insert('jon', (250, 250))
        assert self.tree.is_leaf()
        self.tree.insert('joe', (300, 300))
        assert not self.tree.is_leaf()


class TestQuadTree(TreesTest):
    def setup_method(self):
        self.tree = trees.QuadTree((250, 250))

    def test_height(self):
        assert self.tree.height() == 1
        self.tree.insert('jon', (250, 250))
        assert self.tree.height() == 1
        self.tree.insert('joe', (300, 300))
        assert self.tree.height() == 2
        self.tree.insert('job', (50, 50))
        assert self.tree.height() == 3
        self.tree.insert('0', (25, 25))
        assert self.tree.height() == 5

    def test_depth(self):
        self.tree.insert('jon', (250, 250))
        self.tree.insert('joe', (300, 300))
        self.tree.insert('job', (50, 50))
        self.tree.insert('jay', (25, 25))
        jon = self.tree._nw._se
        joe = self.tree._se
        job = self.tree._nw._nw._nw._se
        jay = self.tree._nw._nw._nw._nw
        assert self.tree.depth(jon) == 2
        assert self.tree.depth(joe) == 1
        assert self.tree.depth(jay) == 4
        assert self.tree.depth(job) == 4
        assert job.depth(jay) is None
        assert self.tree.depth(self.tree) is None


class Test2DTree(TreesTest):
    def setup_method(self):
        self.tree = trees.TwoDTree((0, 0), (500, 500))

    def test_height(self):
        assert self.tree.height() == 1
        self.tree.insert('jon', (250, 250))
        assert self.tree.height() == 1
        self.tree.insert('joe', (300, 300))
        assert self.tree.height() == 2
        self.tree.insert('job', (50, 50))
        assert self.tree.height() == 2
        self.tree.insert('job', (25, 25))
        assert self.tree.height() == 3

    def test_depth(self):
        self.tree.insert('jon', (250, 250))
        self.tree.insert('joe', (300, 300))
        self.tree.insert('job', (50, 50))
        self.tree.insert('minnie_mouse', (50, 100))
        self.tree.insert('jay', (25, 25))
        jon = self.tree
        joe = self.tree._gt
        job = self.tree._lt
        minnie = job._gt
        jay = job._lt
        assert jon.depth(jon) is None
        assert joe.depth(minnie) is None
        assert jon.depth(minnie) == 2
        assert job.depth(minnie) == 1
        assert jon.depth(jay) == 2
        assert job.depth(jay) == 1


if __name__ == '__main__':
    pytest.main(['trees_test.py'])
