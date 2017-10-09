# [START imports]
import os
import urllib

from datetime import datetime
from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from baseClasses import *

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
    	autoescape=True)
# [END imports]
    
# [START LoginPage]
class LoginPage(webapp2.RequestHandler):
 	   def get(self):
        	user = users.get_current_user()
        	if user:
            		nickname = user.nickname()
	    		next_url1 = '/dashboard'
	    		next_url2 = users.create_logout_url('/')
			greeting = 'Welcome, {}'.format(nickname)
	    		button1 = 'Dashboard'
	    		button2 = 'Log Out'
	    		id1 = 'email'
        	else:
            		next_url1 = users.create_login_url('/dashboard')
	    		next_url2 = None
	    		greeting = 'You are logged out. Please sign in to proceed'
	    		button1 = 'Log in'
	    		button2 = None
	    		type1 = None
	    		id1 = None
	
		template_values = {
			'greeting': greeting,
			'url1': next_url1,
	    		'url2': next_url2,
	    		'button1': button1,
	    		'button2': button2
		}	
	
		template = JINJA_ENVIRONMENT.get_template('www/index.html')
		self.response.write(template.render(template_values))
# [END LoginPage]

