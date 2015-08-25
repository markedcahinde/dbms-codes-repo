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
	thesis_author = ndb.StringProperty(indexed=True)
	date = ndb.DateTimeProperty(auto_now_add=True)

class MainPageHandler(webapp2.RequestHandler):

	def get(self):
		user = users.get_current_user()

		if user:
			logout_url = users.create_logout_url('/login')
			link_text = 'Logout'
			template_values = {
				'logout_url':logout_url
			}
			template = JINJA_ENVIRONMENT.get_template('main.html')
		else:
			login_url = users.create_login_url('/home')
			link_text = 'Login'
			template_values = {
				'login_url':login_url
			}
			template = JINJA_ENVIRONMENT.get_template('login.html')

		self.response.write(template.render(template_values))

class APIHandler(webapp2.RequestHandler):
	def get(self):
		thesisdet = thesisentry.query().order(-thesisentry.date).fetch()
		thesis_list = []

		for thesis in thesisdet:
			thesis_list.append({
				'id' : thesis.key.urlsafe(),
				'year': thesis.thesis_year,
				'title': thesis.thesis_title,
				'abstract': thesis.thesis_abstract,
				'adviser': thesis.thesis_adviser,
				'section': thesis.thesis_section,
				'author': thesis.thesis_author
			})
		response = {
			'result' : 'OK',
			'data' : thesis_list
		}

		self.response.headers['Content-Type'] = 'application.json'
		self.response.out.write(json.dumps(response))

	def post(self):

		thesis = thesisentry()
		thesis.thesis_author = users.get_current_user().email()
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
				'author': thesis.thesis_author
			}
		}
		self.response.out.write(json.dumps(response))

# class EditHandler():
# 	def get(self, thesis_id):
# 		the_id = thesisentry.get_by_id(int(thesis_id))
#
# 		response = {
# 			'result' : 'OK',
# 			'data' : the_id
# 		}
#
# 		self.response.headers['Content-Type'] = 'application.json'
# 		self.response.out.write(json.dumps(response))

class LoginHandler(webapp2.RequestHandler):
	def get(self):
		user = users.get_current_user()

		login_url = users.create_login_url('/home')
		template = JINJA_ENVIRONMENT.get_template('login.html')

		template_data = {
			'login_url': login_url
		}

		self.response.write(template.render(template_data))


app = webapp2.WSGIApplication([
	('/api/thesis', APIHandler),
	# ('/edit/(.*)', EditHandler),
	('/login', LoginHandler),
	('/home', MainPageHandler),
	('/', MainPageHandler)
], debug=True)
