# testing_tutorials
This repo contains code from the testing tutorial series on https://blog.miguelgrinberg.com/ 
If you haven't read Miguel's work before, please check him out. His writting style and explanations are top-class and easy to understand.

## file structure
- Each tutorial / blog post has it's own folder.
- part 1: intro to pytest & pytest-cov using the fizz buzz test
- part 2: Pytest using a GUI (replicating the game of life)

## testing approach
- The object-oriented approach based on the TestCase class of the unittest package will be used to structure and organize the unit tests.
- The assert statement from Python will be used to write assertions. The pytest package includes some enhancements to the assert statement to provide more verbose output when there is a failure.
- The pytest test runner will be used to run the tests, as it is required to use the enhanced assert. This test runner has full support for the TestCase class from the unittest package.

## testing libraries used
- pip install pytest  # testing library
- pip install pytest-cov  # shows test coverage
- pip install parameterized  # allows for parameterized testing ("better" than pytest)
