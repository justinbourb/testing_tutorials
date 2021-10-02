import unittest
from flask import current_app
from app import create_app, db
from app.models import User
import os
import re

os.environ['DATABASE_URL'] = 'sqlite://'  # use an in-memory database for tests

class TestWebApp(unittest.TestCase):

	def populate_db(self):
		"""
		helper method
		This function will create a fake user in the database.
		This user can be used later for testing purposes.

		Reasoning:
			Most applications have sections that are restricted to logged in users.  Authentication has a very
			important function besides restricting access, it allows the server to know who the client is.
			In Flask, this would be the current_user variable.  Testing with a fake user account will allow
			tests to function in the same way as the live site.

			The alternate method is to the login requirement, but this is not as effective as outlined above.
		Note:
			the TestCase class will ignore any method that does not start with test_
		"""
		user = User(username='susan', email='susan@example.com')
		user.set_password('foo')
		db.session.add(user)
		db.session.commit()

	def login(self):
		"""
		helper method
		login with our fake user for testing purposes
		"""
		self.client.post('/auth/login', data={
			'username': 'susan',
			'password': 'foo',
		})
	def setUp(self):
		"""
		create an instance of the app
		turn off CSRF for tests. Submitting forms require a CSRF token to validate the form submission as legitimate.
		set the context, which is required by Flask
		push the context to the app
		create a fake database
		setup a test client through Flask
		"""
		self.app = create_app()
		self.app.config['WTF_CSRF_ENABLED'] = False # no CSRF during tests
		self.appctx = self.app.app_context()
		self.appctx.push()
		db.create_all()
		self.populate_db()
		self.client = self.app.test_client()


	def tearDown(self):
		"""
		tear down the app and undo the setup
		"""
		db.drop_all()
		self.appctx.pop()
		self.app = None
		self.appctx = None
		self.client = None

	def test_app(self):
		"""
		This function tests the setUp method.  Expect an app to be created and context pushed to the app.
		"""
		assert self.app is not None
		assert current_app == self.app

	def test_home_page_redirect(self):
		"""
		the get request calls the top level url of the app.  The follow_redirects flag is set because the app
		requires the user to log in, thus it will redirect to the login page.
		"""
		response = self.client.get('/', follow_redirects=True)
		assert response.status_code == 200
		assert response.request.path == '/auth/login'

	def test_registration_form(self):
		"""
		This test spot checks the HTML in the registration page.
		It checks that the registration form has the essential components.
		"""
		response = self.client.get('/auth/register')
		assert response.status_code == 200
		html = response.get_data(as_text=True)
		assert 'name="username"' in html
		assert 'name="email"' in html
		assert 'name="password"' in html
		assert 'name="password2"' in html
		assert 'name="submit"' in html

	def test_register_user(self):
		"""
		The Flask client accepts the form fields in the data argument, using a dictionary.
		The keys of the dictionary must match the form field names.

		create a user,
		redirect them to the login page,
		check heading greet 'Hi, [username]!' in html
		"""
		response = self.client.post('/auth/register', data={
			'username': 'alice',
			'email': 'alice@example.com',
			'password': 'foo',
			'password2': 'foo',
		}, follow_redirects=True)
		assert response.status_code == 200
		assert response.request.path == '/auth/login' # redirect to login

		# login with the new user
		response = self.client.post('/auth/login', data={
			'username': 'alice',
			'password': 'foo',
		}, follow_redirects=True)
		assert response.status_code == 200
		html = response.get_data(as_text=True)
		assert 'Hi, alice!' in html

	def test_register_user_mismatched_password(self):
		"""
		test when users enter two different passwords
		expect: register not successful
		"""
		response = self.client.post('/auth/register', data={
			'username': 'alice',
			'email': 'alice@example.com',
			'password': 'foo',
			'password2': 'bar',
		})
		assert response.status_code == 200
		html = response.get_data(as_Text=True)
		assert 'Field must be equal to password.' in html

	def test_write_post(self):
		"""
		This test will test users posting to the blog.
		"""
		self.login()
		response = self.client.post('/', data={
			'post': 'Hello, world!'
		}, follow_redirects=True)
		assert response.status_code == 200
		html = response.get_data(as_text=True)
		assert 'Your post is now live!' in html
		assert 'Hello, world!' in html
		assert re.search(r'span class="user_popup">\s*'
		                 r'<a href="/user/susan">\s*'
		                 r'susan\s*</a>\s*</span>\s*said', html) is not None
