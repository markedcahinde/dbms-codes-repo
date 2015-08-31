import webapp2
from google.appengine.api import users
from google.appengine.ext import ndb
import jinja2
import os
import logging
import json

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)

class thesisentry(ndb.Model):
	thesis_year = ndb.IntegerProperty()
	thesis_title = ndb.StringProperty(indexed=True)
	thesis_abstract = ndb.StringProperty(indexed=True)
	thesis_adviser = ndb.StringProperty(indexed=True)
	thesis_section = ndb.IntegerProperty()
	thesis_author = ndb.KeyProperty(kind='User',indexed=True)
	date = ndb.DateTimeProperty(auto_now_add=True)

class User(ndb.Model):
	email = ndb.StringProperty(indexed=True)
	first_name = ndb.StringProperty()
	last_name = ndb.StringProperty()
	phone_number = ndb.IntegerProperty()
	created_date = ndb.DateTimeProperty(auto_now_add=True)

class MainPageHandler(webapp2.RequestHandler):

	def get(self):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get().first_name
			if user:
				logout_url = users.create_logout_url('/')
				link_text = 'Logout'
				template_values = {
					'logout_url':logout_url,
					'user':user
				}
				template = JINJA_ENVIRONMENT.get_template('main.html')
				self.response.write(template.render(template_values))
			else:
				self.redirect('/register')

		else:
			login_url = users.create_login_url('/login')
			template_values = {
				'login_url':login_url,
				'reg_url':'/register'
			}
			template = JINJA_ENVIRONMENT.get_template('login.html')
			self.response.write(template.render(template_values))

class APIHandler(webapp2.RequestHandler):
	def get(self):
		thesisdet = thesisentry.query().order(-thesisentry.date).fetch()
		thesis_list = []
		logging.info(thesisdet)
		for thesis in thesisdet:
			user = User.query(User.key == thesis.thesis_author)
			e = []
			for u in user:
				e.append({
					'first_name':u.first_name,
					'last_name':u.last_name
				})
			thesis_list.append({
				'id' : thesis.key.urlsafe(),
				'year': thesis.thesis_year,
				'title': thesis.thesis_title,
				'abstract': thesis.thesis_abstract,
				'adviser': thesis.thesis_adviser,
				'section': thesis.thesis_section,
				'author': e

			})
		response = {
			'result' : 'OK',
			'data' : thesis_list
		}

		self.response.headers['Content-Type'] = 'application.json'
		self.response.out.write(json.dumps(response))

	def post(self):

		thesis = thesisentry()
		user = User()
		loggedin_user = users.get_current_user()
		user_key = ndb.Key('User', loggedin_user.user_id())
		thesis.thesis_author = user_key
		thesis.thesis_year = int(self.request.get('thesis_year'))
		thesis.thesis_title = self.request.get('thesis_title')
		thesis.thesis_abstract = self.request.get('thesis_abstract')
		thesis.thesis_adviser = self.request.get('thesis_adviser')
		thesis.thesis_section = int(self.request.get('thesis_section'))
		thesis.put()

		self.response.headers['Content-Type'] = 'application/json'
		response = {
			'result': 'OK',
			'data': {
				'id' : thesis.key.urlsafe(),
				'year': thesis.thesis_year,
				'title': thesis.thesis_title,
				'abstract': thesis.thesis_abstract,
				'adviser': thesis.thesis_adviser,
				'section': thesis.thesis_section,
				'author': user_key.get().first_name + ' ' + user_key.get().last_name
			}
		}
		self.response.out.write(json.dumps(response))

class LoginHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()
		if user:
			user_key = ndb.Key('User', user.user_id())
			user_info = user_key.get()
			if user_info:
				self.redirect('/home')
			else:
				self.redirect('/register')

class RegistrationHandler(webapp2.RequestHandler):
	def get(self):
		loggedin_user = users.get_current_user()
		if loggedin_user:
			user_key = ndb.Key('User', loggedin_user.user_id())
			user = user_key.get()
			if user:
				self.redirect('/home')
			else:
				template_data = {
					'email':loggedin_user.email()
				}
				template = JINJA_ENVIRONMENT.get_template('register.html')
				self.response.write(template.render(template_data))
		else:
			self.redirect(users.create_login_url('/register'))

	def post(self):
		user = User(id=users.get_current_user().user_id())
		user.phone_number = int(self.request.get('phone_number'))
		user.email = self.request.get('email')
		user.first_name = self.request.get('first_name')
		user.last_name = self.request.get('last_name')
		user.put()
		self.response.headers['Content-Type'] = 'application/json'
		response = {
			'result':'OK',
			'data':{
				'first_name':user.first_name,
				'last_name':user.last_name,
				'phone_number':user.phone_number,
				'id':users.get_current_user().user_id()
			}
		}
		self.response.out.write(json.dumps(response))

app = webapp2.WSGIApplication([
	('/api/thesis', APIHandler),
	('/register', RegistrationHandler),
	('/login', LoginHandler),
	('/home', MainPageHandler),
	('/', MainPageHandler)
], debug=True)
