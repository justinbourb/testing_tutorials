#!/usr/bin/env python
from datetime import datetime, timedelta
import unittest
from app import create_app, db
from app.models import User, Post
from config import Config
"""
This file tests 
    Password hashing
    Generation of user avatar URLs
    Followers
    Timeline of followed posts
Their explanation can be found in the Flask Mega Tutorial
The only requirement to exercise these parts of the application is access to a database,
and in fact, these four tests target functionality that can be accessed from the User 
model alone. There is no need to invoke web routes, render templates, or work with a 
web requests, so this type of tests are the simplest to create, and can be targeted to 
the basic building blocks of your application, those that cannot fail under any 
circumstance.

The setUp() and tearDown() methods are special methods that the unit testing framework 
executes before and after each test respectively. I have implemented a little hack in 
setUp(), to prevent the unit tests from using the regular database that I use for 
development. By changing the application configuration to sqlite:// I get SQLAlchemy 
to use an in-memory SQLite database during the tests. The db.create_all() call creates 
all the database tables. This is a quick way to create a database from scratch that is 
useful for testing

The new application will be stored in self.app, but creating an application isn't 
enough to make everything work. Consider the db.create_all() statement that creates the 
database tables. The db instance needs to know what the application instance is, because 
it needs to get the database URI from app.config, but when you are working with an 
application factory you are not really limited to a single application, there could be 
more than one created. So how does db know to use the self.app instance that I just 
created?

The answer is in the application context. Remember the current_app variable, which 
somehow acts as a proxy for the application when there is no global application to 
import? This variable looks for an active application context in the current thread, 
and if it finds one, it gets the application from it. If there is no context, then 
there is no way to know what application is active, so current_app raises an exception.

"""

class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    ELASTICSEARCH_URL = None


class UserModelCase(unittest.TestCase):
    def setUp(self):
        # create an app for each test run
        self.app = create_app(TestConfig)
        # set the context so the db targets this new app
        self.app_context = self.app.app_context()
        # push the context to the created app so db.create_all() will work
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        # do the opposite of setUp
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_password_hashing(self):
        u = User(username='susan')
        u.set_password('cat')
        self.assertFalse(u.check_password('dog'))
        self.assertTrue(u.check_password('cat'))

    def test_avatar(self):
        u = User(username='john', email='john@example.com')
        self.assertEqual(u.avatar(128), ('https://www.gravatar.com/avatar/'
                                         'd4c74594d841139328695756648b6bd6'
                                         '?d=identicon&s=128'))

    def test_follow(self):
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        db.session.add(u1)
        db.session.add(u2)
        db.session.commit()
        self.assertEqual(u1.followed.all(), [])
        self.assertEqual(u1.followers.all(), [])

        u1.follow(u2)
        db.session.commit()
        self.assertTrue(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 1)
        self.assertEqual(u1.followed.first().username, 'susan')
        self.assertEqual(u2.followers.count(), 1)
        self.assertEqual(u2.followers.first().username, 'john')

        u1.unfollow(u2)
        db.session.commit()
        self.assertFalse(u1.is_following(u2))
        self.assertEqual(u1.followed.count(), 0)
        self.assertEqual(u2.followers.count(), 0)

    def test_follow_posts(self):
        # create four users
        u1 = User(username='john', email='john@example.com')
        u2 = User(username='susan', email='susan@example.com')
        u3 = User(username='mary', email='mary@example.com')
        u4 = User(username='david', email='david@example.com')
        db.session.add_all([u1, u2, u3, u4])

        # create four posts
        now = datetime.utcnow()
        p1 = Post(body="post from john", author=u1,
                  timestamp=now + timedelta(seconds=1))
        p2 = Post(body="post from susan", author=u2,
                  timestamp=now + timedelta(seconds=4))
        p3 = Post(body="post from mary", author=u3,
                  timestamp=now + timedelta(seconds=3))
        p4 = Post(body="post from david", author=u4,
                  timestamp=now + timedelta(seconds=2))
        db.session.add_all([p1, p2, p3, p4])
        db.session.commit()

        # setup the followers
        u1.follow(u2)  # john follows susan
        u1.follow(u4)  # john follows david
        u2.follow(u3)  # susan follows mary
        u3.follow(u4)  # mary follows david
        db.session.commit()

        # check the followed posts of each user
        f1 = u1.followed_posts().all()
        f2 = u2.followed_posts().all()
        f3 = u3.followed_posts().all()
        f4 = u4.followed_posts().all()
        self.assertEqual(f1, [p2, p4, p1])
        self.assertEqual(f2, [p2, p3])
        self.assertEqual(f3, [p3, p4])
        self.assertEqual(f4, [p4])


if __name__ == '__main__':
    unittest.main(verbosity=2)
