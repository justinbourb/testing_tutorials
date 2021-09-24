import unittest  # pip install pytest
from fizzbuzz import fizzbuzz


class TestFizzBuzz(unittest.TestCase):
	"""
	Purpose: run the 'pytest' command in the terminal and it will automatically detect any files named test_something.py
	or something_test.py and look for unit tests to run provided the files are in the same directory.
	Tests can be stored in a separate package from the source code.
	"""

	def test_fizz(self):
		"""
		Purpose: test results divisible by 3
		:return:
		"""
		for i in [3, 6, 9, 18]:
			print('testing', i)
			assert fizzbuzz(i) == 'Fizz'

	def test_buzz(self):
		"""
		Purpose: test results divisible by 5
		:return:
		"""
		for i in [5, 10, 50]:
			print('testing', i)
			assert fizzbuzz(i) == 'Buzz'

	def test_fizzbuzz(self):
		"""
		Purpose: test results divisible by 15
		:return:
		"""
		for i in [15, 30, 75]:
			print('testing', i)
			assert fizzbuzz(i) == 'FizzBuzz'

	def test_number(self):
		"""
		Purpose: test results not divisible by 3, 5 or 15
		:return:
		"""
		for i in [2, 4, 88]:
			print('testing', i)
			assert fizzbuzz(i) == i