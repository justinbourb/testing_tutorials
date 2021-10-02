import unittest
from flask import current_app
from app import create_app, db
import os

os.environ['DATABASE_URL'] = 'sqlite://'  # use an in-memory database for tests

class TestWebApp(unittest.TestCase):

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
		response = self.client.post('/auth/register', data={
			'username': 'alice',
			'email': 'alice@example.com',
			'password': 'foo',
			'password2': 'foo',
		}, follow_redirects=True)
		assert response.status_code == 200
		assert response.request.path == '/auth/login' # redirect to login

		# login with the new user
		respone = self.client.post('/auth/login', data={
			'username': 'alice',
			'password': 'foo',
		}, follow_redirects=True)
		assert response.status_code == 200
		html = response.get_data(as_text=True)
		assert 'Hi, alice!' in html

