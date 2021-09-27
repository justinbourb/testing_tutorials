## This repo is based on Miguel Grinberg unit_testing blog part 2 
- Mr. Grinberg's blog for this project: https://blog.miguelgrinberg.com/post/how-to-write-unit-tests-in-python-part-2-game-of-life
- Mr. Grinberg's github for this project is here: https://github.com/miguelgrinberg/python-testing/blob/main/life/life.py.
- The game is based on: https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life


## Running the Simulation
Before we get into the specifics of how to test this code, you may want to play with it. Follow these steps to get it set up on your computer:

- Clone the GitHub repository.
- Create a virtual environment and install pygame on it, the only third-party dependency.
- Change to the life directory
- Run python life_gui.py [pattern-file] to start a simulation. There are many interesting patterns to try in the patterns sub-directory. The example pattern you see at the top of this article can be started with the command python life_gui.py patterns/pentadecathlon.txt. If a pattern file isn't provided, the simulation starts on an empty grid.

### Once the simulation is running, there are a few keys that you can use:

- Space to pause and resume the simulation
- Esc to exit
- Arrow keys to scroll through the infinite grid
- + and - to zoom in or out
- c to center the grid
- Mouse click on a cell to toggle its state (you may want to do this while the simulation is paused)

## notes
- pip install parameterized 
- parameterized runs the same test with different inputs
    - @parameterized.expand([('pattern1.txt',), ('pattern2.txt',)])
      def test_load_life_1_05(self, pattern):
- itertools will create test matrix with all combinations of input
    - import itertools  
        list(itertools.product([True, False], range(9)))  
        [(True, 0), (True, 1), ..., (False, 0), (False, 1), etc]
- Mocking
    - from unittest import mock
    - Mocking is the process of creating fake inputs or outputs for 
    functions.  
    - This is helpful in testing functions that call other 
    functions.
    - unittest mock can also record the number of calls being made
        - fake.call_args_list()
    - The mock package provides a few patching functions to inject
    the fake function into the part of the application we want to test.
        - @mock.patch.object(Life, '_advance_cell')
        - @mock.patch.object(testing_object, function_to_mock)        