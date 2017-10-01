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


# [START Dashboard]
class Dashboard(webapp2.RequestHandler):
    	def get(self):
        	user = users.get_current_user()
       		if user:
            		project_query = Project.query()
            		projects = project_query.fetch(10)
            		template_values = {
                		'greeting': 'Dashboard',
                		'url1': ('/create'),
		                'url2': users.create_logout_url('/'),
                		'button1': 'New Project',
		                'button2': 'Logout',
                		'projects': projects
                	}
            		template = JINJA_ENVIRONMENT.get_template('www/dashboard.html')
            		self.response.write(template.render(template_values))
        	else:
            		template_values = {
                		'greeting': 'You are logged out. Please sign in to proceed',
                		'url1': users.create_login_url('/dashboard'),
                		'button1': 'Login',
                		'button2': None
                	}
            	template = JINJA_ENVIRONMENT.get_template('www/index.html')
            	self.response.write(template.render(template_values))

	def post(self):
        	strKey = self.request.get('key')
        	page = self.request.get('page')
        	newKey = stringToKey(strKey)
		if self.request.POST.get('delete', None):
            		newKey.delete()
            		self.redirect('/dashboard')
        	elif self.request.POST.get('edit', None):
            		self.redirect('/create?id='+strKey)
		elif self.request.POST.get('run',None):
            		self.redirect('/run?id='+strKey)

# [End Dashboard]
