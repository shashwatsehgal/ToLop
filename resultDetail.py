# [START imports]
import os
import urllib

import ebaysdk
from ebaysdk.finding import Connection as finding

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

# [START ResultDetail]
class ResultDetail(webapp2.RequestHandler):
	def get(self):
		# Gets the current user details and checks whether the user has logged in or not
                user = users.get_current_user()
		if user:
			# User has logged in correctly
			# Reads the result from the datastore
			strKey = self.request.get('id')
                	projectKey = stringToKey(strKey, 'Project')
                	page = self.request.get('page')
	                strItemKey = self.request.get('item')
			itemKey = stringToKeyWithParent(strItemKey, 'Project', 'SearchResult')
			item = itemKey.get()
			# Send the template to the details.html page	
	                template_values = {
				'greeting': 'Details for: '+item.title,
				'projectKey': projectKey,
				'page': page,
				'searchItem': item,
				'itemKey': itemKey
			}
			template = JINJA_ENVIRONMENT.get_template('www/details.html')
             		self.response.write(template.render(template_values))
                else:
                        # Not logged in. Redirects to login page
                        template_values = {
                                'greeting': 'You are logged out. Please sign in to proceed',
                                'url1': users.create_login_url('/dashboard'),
                                'button1': 'Login',
                                'button2': None,
                        }
                        template = JINJA_ENVIRONMENT.get_template('www/index.html')
                        self.response.write(template.render(template_values))

	def post(self):
	        strKey = self.request.get('projectKey')
                projectKey = stringToKey(strKey, 'Project')
                page = self.request.get('page')
                strItemKey = self.request.get('itemKey')
                itemKey = stringToKeyWithParent(strItemKey, 'Project', 'SearchResult')
                item = itemKey.get()
		if self.request.POST.get('results', None):
			self.redirect('/run?id='+strKey+'&page='+page)
		else:
			if self.request.POST.get('safe', None):
                        	item.searchStatus = 'Safe'
	                elif self.request.POST.get('suspicious', None):
        	                item.searchStatus = 'Suspicious'
                	elif self.request.POST.get('new', None):
       	                 item.searchStatus = 'New'
			elif self.request.POST.get('newComment', None):
				item.comments = item.comments+'\nOn '+datetime.now().strftime("%Y-%m-%d")+', '+users.get_current_user().nickname()+" wrote: "+self.request.POST.get('newComment',None)+'\n--------------------------------------------------------------------------------\n'
			item.put()
			self.redirect('/details?id='+strKey+'&page='+page+'&item='+strItemKey)


