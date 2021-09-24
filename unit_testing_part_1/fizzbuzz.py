def fizzbuzz(i):
	"""
	Purpose: This function accepts an int, i and returns:
	    1) FizzBuzz if the number is divisible by 5 & 3.
	    2) Fizz if the number is divisible by 3.
	    3) Buzz if the number is divisible by 5.
	    4) The number if it is not divisible by 3, 5 or 3 & 5.
	:param i: an int
	:return:
		1) FizzBuzz if the number is divisible by 5 & 3.
	    2) Fizz if the number is divisible by 3.
	    3) Buzz if the number is divisible by 5.
	    4) The number if it is not divisible by 3, 5 or 3 & 5.
	"""

	if i % 15 == 0:
		return "FizzBuzz"
	elif i % 3 == 0:
		return "Fizz"
	elif i % 5 == 0:
		return "Buzz"
	else:
		return i


def main():
	for i in range(1, 101):
		print(fizzbuzz(i))


"""
standard top-level script check so that this function is automatically executed when the script is run directly, 
but not when it is imported by another script. 
"""
if __name__ == '__main__':
	main()
