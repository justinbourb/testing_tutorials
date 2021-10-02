## This repo is based on Miguel Grinberg unit_testing blog part 3 
This repo contains code from the testing tutorial series on https://blog.miguelgrinberg.com/ 
If you haven't read Miguel's work before, please check him out. His writing style and
 explanations are top-class and easy to understand.
This is the third part in the series about unit testing Python applications.
Concepts shown  are universal to web apps and can be applied to other frameworks as well.

- Mr. Grinberg's blog for this project: https://blog.miguelgrinberg.com/post/how-to-write-unit-tests-in-python-part-3-web-applications
- Mr. Grinberg's github for this project is here: https://github.com/miguelgrinberg/microblog

## Setting up the environment
- Download this repo to your local environment and install the requirement listed in requirements.txt
    - pip install -r requirements.txt
- This repo was created using PyCharm IDE
- You may want to set up a virtual environment with PyCharm under File -> Settings -> Project
 -> Python Interpreter
- (venv) $ pip install pytest pytest-cov

## testing libraries
Pytest will be used to run the unit tests.
- pip install pytest
Pytest-cov will be used to check test coverage, it reports lines which were not run during testing.
- pip install pytest-cov

## Starting up the app
- (venv) $ flask db upgrade
- (venv) $ flask run

## Running tests
### with pytest

- (venv) $ pytest --cov=app --cov-report=term-missing --cov-branch test*
- (venv) $ pytest --cov=app --cov-report=term-missing --cov-branch
### with unittest
- (venv) $ python tests.py

## notes
- the setUp() and tearDown() methods are special methods for the unit testing framework
that get run before and after each test.  They are being used to create a fake database for
testing purposes.
- The new application will be stored in self.app, but creating an application isn't 
enough to make everything work. Consider the db.create_all() statement that creates the 
database tables. The db instance needs to know what the application instance is, because 
it needs to get the database URI from app.config, but when you are working with an 
application factory you are not really limited to a single application, there could be 
more than one created. So how does db know to use the self.app instance that I just 
created?

- The answer is in the application context. Remember the current_app variable, which 
somehow acts as a proxy for the application when there is no global application to 
import? This variable looks for an active application context in the current thread, 
and if it finds one, it gets the application from it. If there is no context, then 
there is no way to know what application is active, so current_app raises an exception.

- Python Flask uses Web Server Gateway Interface (WSGI) to communicate between a web server and the web app.  Another
popular framework is Asynchronous Server Gateway Interface (ASGI).  WSGI and AGSI have specific rules on how information
must be passed, this allows unit tests to follow the same procedures to inject fake requests into the application during
testing.
    - WGSI provides the Werkzerug package for testing
    - AGSI provides async-asgi-testclient for testing 

