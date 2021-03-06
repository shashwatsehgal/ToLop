# [START imports]
import os
import urllib

from datetime import datetime
from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from baseClasses import *
from authModel import *
from authBaseCode import *

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
    	autoescape=True)
# [END imports]
    
# [START LoginPage]
class NewUser(BaseHandler):
	def get(self):
		params = { 'greeting': 'Enter new user details'}
		template = JINJA_ENVIRONMENT.get_template('www/register.html')
		self.response.write(template.render(params))

  	def post(self):
    		user_name = self.request.get('username')
		email = self.request.get('email')
    		name = self.request.get('name')
    		password = self.request.get('password')
    		last_name = self.request.get('lastname')
		company = self.request.get('company')

    		unique_properties = ['email_address']
    		user_data = self.user_model.create_user(user_name,
      			unique_properties,
      			email_address=email, name=name, password_raw=password,
      			last_name=last_name, company=company, verified=False)
    
    		greeting = ""
		if not user_data[0]: #user_data is a tuple
      			greeting = ('Unable to create account: User %s already exists!' % (user_name))
   		else:
			user = user_data[1]
			user.put()
			greeting = ('Success! Please continue to Login')
		params = { 'greeting': greeting }
		template = JINJA_ENVIRONMENT.get_template('www/register.html')
		self.response.write(template.render(params))
