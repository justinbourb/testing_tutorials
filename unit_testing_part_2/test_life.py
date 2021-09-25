import unittest

import pytest
from parameterized import parameterized

from life import CellList, Life

class TestCellList(unittest.TestCase):
    def test_empty(self):
        """
        Test that an empty cell list is empty
        :return:
        """
        c = CellList()
        assert list(c) == []

    def test_set_true(self):
        """
        The True flag for c.set() should add the items to the CellList.
        Add cells to the CellList and test if they are actually in the list.
        :return:
        """
        c = CellList()
        c.set(1, 2, True)
        assert c.has(1, 2)
        assert list(c) == [(1, 2)]
        c.set(500, 600, True)
        assert c.has(1, 2) and c.has(500, 600)
        assert list(c) == [(1, 2), (500, 600)]
        c.set(1, 2, True)  # make sure a cell can be set to True twice
        assert c.has(1, 2) and c.has(500, 600)
        assert list(c) == [(1, 2), (500, 600)]

    def test_set_false(self):
        """
        The Flase flag for c.set() should *not* add the items to the CellList.
        Add cells to the CellList using False and test if they are *not* in the list.
        :return:
        """
        c = CellList()
        c.set(1, 2, False)
        assert not c.has(1, 2)
        assert list(c) == []
        c.set(1, 2, True)
        c.set(1, 2, False)
        assert not c.has(1, 2)
        assert list(c) == []
        c.set(1, 2, True)
        c.set(3, 2, True)
        c.set(1, 2, False)  # using False also removes items from the list
        assert not c.has(1, 2)
        assert c.has(3, 2)
        assert list(c) == [(3, 2)]

    def test_set_default(self):
        """
        The value argument of the set() method can also be omitted, in which case the method works as a toggle.
        :return:
        """
        c = CellList()
        c.set(1, 2)
        assert c.has(1, 2)
        assert list(c) == [(1, 2)]
        c.set(1, 2)
        assert not c.has(1, 2)
        assert list(c) == []
class TestLife(unittest.TestCase):
        def test_new(self):
            """
            making sure that a brand new object has a sound structure and that should take care of the constructor method.
            This includes making sure that the survival and birth attributes are set correctly and that the grid of the
            game is completely empty.
            Note: testing life.alive returns an object, which is why we call list(life.living_cells()) instead
            """
            life = Life()
            assert life.survival == [2, 3]
            assert life.birth == [3]
            assert list(life.living_cells()) == []
            assert life.rules_str() == '23/3'

        def test_new_custom(self):
            """
            Test creating a game with a custom ruleset
            :return:
            """
            life = Life([3, 4], [4, 7, 8])
            assert life.survival == [3, 4]
            assert life.birth == [4, 7, 8]
            assert list(life.living_cells()) == []
            assert life.rules_str() == '34/478'

        """
        load() logic:
            1) opens a file to load a pattern for creating a game Life() object
            2) reads the file and checks the header
                a) if header = #Life 1.05
                    1) if line.startswith('#D') continue
                    2) elif line.startswith('#N') create a game with default parameters
                    3) elif line.startswith('#R') create a game with custom parameters formatted with '/' split
                    4) elif line.startswith('#P') grid location x y expected format 10 15
                    5) else find all the starting points to populate the world with 
                b) elif header = #Life 1.06
                    1) find all the starting points to populate the world with
                c) else raise an error, file format unknown / unspecified

        pattern test files:
            pattern1: Life 1.05 default parameters
            pattern2: Life 1.06
            pattern3: Life 1.05 custom parameters
            pattern4: unknown format / unspecified
        """

        # parameterized runs the same test with different inputs
        @parameterized.expand([('pattern1.txt',), ('pattern2.txt',)])
        def test_load_life_1_05_or_06(self, pattern):
            life = Life()
            life.load(pattern)
            assert life.survival == [2, 3]
            assert life.birth == [3]
            assert set(life.living_cells()) == {(10, 10), (11, 11), (15, 10), (17, 10)}
            assert life.rules_str() == '23/3'
            assert life.bounding_box() == (10, 10, 17, 11)

        def test_load_life_custom(self):
            life = Life()
            life.load('pattern3.txt')
            assert life.survival == [3, 4]
            assert life.birth == [4, 5]
            assert set(life.living_cells()) == {(10, 10), (10, 12), (11, 11)}
            assert life.rules_str() == '34/45'
            assert life.bounding_box() == (10, 10, 11, 12)

        def test_load_runtime_error(self):
            life = Life()
            # loading this file will create an error, pytest is able to catch these for testing purposes
            with pytest.raises(RuntimeError):
                life.load('pattern4.txt')

        def test_toggle(self):
            life = Life()
            # test toggling dead cells to alive
            life.toggle(10, 10)
            assert set(life.living_cells()) == {(10, 10)}
            # test toggling alive cells to dead
            life.toggle(10, 10)
            assert list(life.living_cells()) == []


