# testing_tutorials
This repo contains code from the testing tutorial series on https://blog.miguelgrinberg.com/
If you haven't read Miguel's work before, please check him out.  His writting style and explanations are top-class and easy to understand.

## Setting up the environment
- Download this repo to your local environment and install the requirement listed in requirements.txt
- This repo was created using PyCharm IDE

## testing libraries
Pytest will be used to run the unit tests.
- pip install pytest
Pytest-cov will be used to check test coverage, it reports lines which were not run during testing.
- pip install pytest-cov

## testing approach
- The object-oriented approach based on the TestCase class of the unittest package will be used to structure and organize the unit tests.
- The assert statement from Python will be used to write assertions. The pytest package includes some enhancements to the assert statement to provide more verbose output when 
there is a failure.
- The pytest test runner will be used to run the tests, as it is required to use the enhanced assert. This test runner has full support for the TestCase class from the unittest 
package.

## notes
- The pytest command is smart and automatically detects unit tests. In general it will assume that any Python files named with the test_[something].py or [something]_test.py 
patterns contain unit tests. It will also look for files with this naming pattern in subdirectories. A common way to keep unit tests nicely organized in a larger project is to 
put them in a tests package, separately from the application source code.

## Running unit tests with pytest
- Running pytest with all passing tests
![image](https://github.com/justinbourb/testing_tutorials/blob/master/unit_testing_part_1/images/pytest_passing%20test.JPG)
- Running pytest with failing tests
![image](https://github.com/justinbourb/testing_tutorials/blob/master/unit_testing_part_1/images/pytest_failing_test.JPG)
- Running pytest with code coverage
![image](https://github.com/justinbourb/testing_tutorials/blob/master/unit_testing_part_1/images/pytest_test_coverage.JPG)
- The package or module should be specified when testing code coverage, else Python standard libraries will be included in the output (usually not desired).
![image](https://github.com/justinbourb/testing_tutorials/blob/master/unit_testing_part_1/images/pytest_test_coverage_unspecified.JPG)
- pytest can report in several formats
![image](https://github.com/justinbourb/testing_tutorials/blob/master/unit_testing_part_1/images/pytest_test_coverage_report_missing.JPG)


