import itertools
import random
import unittest
from unittest import mock

import pytest
from parameterized import parameterized

from life import CellList, Life

# pytest --cov=life --cov-report=term-missing --cov-branch


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

        """
        test_advance_cell will start with a target cell (0,0) and will test the surrounding 8 cells
        (0,0) are represented as 0, surround cells are represented as X
         X X X            
         X 0 X
         X X X
         A random number of neighbors will be tested to test all possible combinations.
         
         1) @parameterized decorator is used to run the same test with multiple inputs
         2) itertools is used to create a test matrix.  The test will be run on all combinations of True/False
            and range(9)
                import itertools  
                list(itertools.product([True, False], range(9)))  
                [(True, 0), (True, 1), ..., (False, 0), (False, 1), etc]
        3) A default and custom rule for birth and survival are also tested
        
        This parametrized test is now handling 2 x 2 x 2 x 9 = 72 different tests
        """

        @parameterized.expand(itertools.product(
            [[2, 3], [4]],  # two different survival rules
            [[3], [3, 4]],  # two different birth rules
            [True, False],  # two possible states for the cell
            range(0, 9),  # nine number of possible neighbors
        ))
        def test_advance_cell(self, survival, birth, alive, num_neighbors):
            life = Life(survival, birth)
            if alive:
                life.toggle(0, 0)
            neighbors = [(-1, -1), (0, -1), (1, -1),
                         (-1, 0), (1, 0),
                         (-1, 1), (0, 1), (1, 1)]
            for i in range(num_neighbors):
                n = random.choice(neighbors)
                neighbors.remove(n)
                life.toggle(*n)

            new_state = life._advance_cell(0, 0)
            if alive:
                # survival rule
                if num_neighbors in survival:
                    assert new_state is True
                else:
                    assert new_state is False
            else:
                # birth rule
                if num_neighbors in birth:
                    assert new_state is True
                else:
                    assert new_state is False

        """
        from unittest import mock
        @mock allows creating fake functions and passing them to unit tests
        using the .patch.object(test, function_to_mock) format.
        This allows testing of functions that call other functions in a more reliable manner.
        Mock also allows tracking the number of times the fake function is called to test
        program performance.
        mock_advance_cell.call_count == 24
        mock_function.call_count
        
        test_advance_false uses the following grid:
        x x x x x                 x x x
        x O x O x                 x O x 
        x x x x x                 x x x 
        """
        @mock.patch.object(Life, '_advance_cell')
        def test_advance_false(self, mock_advance_cell):
            mock_advance_cell.return_value = False
            life = Life()
            life.toggle(10, 10)
            life.toggle(12, 10)
            life.toggle(20, 20)
            life.advance()

            # there should be exactly 24 calls to _advance_cell:
            # - 9 around the (10, 10) cell
            # - 6 around the (12, 10) cell (3 were already processed by (10, 10))
            # - 9 around the (20, 20) cell
            assert mock_advance_cell.call_count == 24
            assert list(life.living_cells()) == []

        """
        from unittest import mock
        @mock allows creating fake functions and passing them to unit tests
        using the .patch.object(test, function_to_mock) format.
        This allows testing of functions that call other functions in a more reliable manner.
        Mock also allows tracking the number of times the fake function is called to test
        program performance.
        mock_advance_cell.call_count == 24
        mock_function.call_count

        test_advance_false uses the following grid:
        x x x x                 x x x
        x O O x                 x O x 
        x x x x                 x x x 
        """
        @mock.patch.object(Life, '_advance_cell')
        def test_advance_true(self, mock_advance_cell):
            mock_advance_cell.return_value = True
            life = Life()
            life.toggle(10, 10)
            life.toggle(11, 10)
            life.toggle(20, 20)
            life.advance()

            # there should be exactly 24 calls to _advance_cell:
            # - 9 around the (10, 10) cell
            # - 3 around the (11, 10) cell (3 were already processed by (10, 10))
            # - 9 around the (20, 20) cell
            assert mock_advance_cell.call_count == 21

            # since the mocked advance_cell returns True in all cases, all 24
            # cells must be alive
            assert set(life.living_cells()) == {
                (9, 9), (10, 9), (11, 9), (12, 9),
                (9, 10), (10, 10), (11, 10), (12, 10),
                (9, 11), (10, 11), (11, 11), (12, 11),
                (19, 19), (20, 19), (21, 19),
                (19, 20), (20, 20), (21, 20),
                (19, 21), (20, 21), (21, 21),
            }
