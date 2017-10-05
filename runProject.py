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

from markupsafe import Markup

def urlencode(s):
	if type(s) == 'Markup':
        	s = s.unescape()
    	s = s.encode('utf8')
    	s = urllib.quote_plus(s)
    	return Markup(s)

# [START RunProject]
class RunProject(webapp2.RequestHandler):
	def get(self):
		strKey = self.request.get('id')
		currentPage = self.request.get('page')
		newKey = stringToKey(strKey)
		resultsPerPage = 10
		existingProject = newKey.get()
		api = finding(siteid ='EBAY-US', appid='Shashwat-ToLoP-PRD-35d80d3bd-64e84449', config_file=None)
		api.execute('findItemsAdvanced', {
			'keywords': ['toys r us '+existingProject.projectName],
			'buyerPostalCode': existingProject.zipCode,
			'itemFilter': [
        			{'name': 'ListedIn', 'value': 'EBAY-US'},
        			{'name': 'LocatedIn', 'value': 'US'},
        			{'name': 'Condition', 'value': 'New'},
				{'name': 'MaxDistance', 'value': '100'}
    			],
    			'sortOrder': 'DistanceNearest'
		})
 	
		if hasattr(api.response.reply, 'paginationOutput'):
			numResults = api.response.reply.paginationOutput.totalEntries
			numPages = (int(numResults) - int(numResults) % resultsPerPage)//resultsPerPage+ 1 
			dictstr = api.response.reply.searchResult
			template_values = {
				'numResults': numResults,
				'numPages': numPages,
				'projectID': strKey,
				'currentPage': currentPage,
				'resultsPerPage': resultsPerPage,
				'greeting': 'Results: '+numResults+' posts found on eBay',
                       		'url2': ('/dashboard'),
       	        	        'button1': 'Save Results',
        	                'button2': 'Return to Dashboard',
                  		'searchResults': dictstr.item
                	}
		else:
			template_values = {
				'numResults': 0,
				'numPages': 0,
				'projectID': strKey,
				'currentPage': currentPage,
				'resultsPerPage': resultsPerPage,
				'greeting': 'Results: 0 posts found on eBay',
                        	'url2': ('/dashboard'),
     	        	        'button1': 'Save Results',
        	                'button2': 'Return to Dashboard'
			}

		JINJA_ENVIRONMENT.filters['urlencode'] = urlencode
                template = JINJA_ENVIRONMENT.get_template('www/results.html')
                self.response.write(template.render(template_values))		
