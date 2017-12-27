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


# [START Dashboard]
class Dashboard(BaseHandler):
    	@user_required
	def get(self):
            	project_query = Project.query()
            	projects = project_query.fetch(10)
		watchedSellers_query = WatchedSeller.query()
		watchedSellers = watchedSellers_query.fetch()
            	template_values = {
                	'greeting': 'Dashboard',
                	'url1': ('/create'),
                	'projects': projects,
			'watchedSellers': watchedSellers
                }
            	template = JINJA_ENVIRONMENT.get_template('www/dashboard.html')
            	self.response.write(template.render(template_values))

	def post(self):
        	strKey = self.request.get('key')
        	page = self.request.get('page')
        	newKey = stringToKey(strKey, 'Project')
		if self.request.POST.get('delete', None):
            		searchQuery = SearchResult.query(ancestor = newKey)
			searchResults = list(searchQuery.fetch())
			for item in searchResults:
				item.key.delete()
			newKey.delete()
            		self.redirect('/dashboard')
        	elif self.request.POST.get('edit', None):
            		self.redirect('/create?id='+strKey)
		elif self.request.POST.get('run',None):
            		self.redirect('/run?id='+strKey+'&page=1')

# [End Dashboard]
