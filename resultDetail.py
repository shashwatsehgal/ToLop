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
		strKey = self.request.get('id')
                projectKey = stringToKey(strKey, 'Project')
                page = self.request.get('page')
                strItemKey = self.request.get('item')
                print "\nKey: %s"%strItemKey
		itemKey = stringToKeyWithParent(strItemKey, 'Project', 'SearchResult')
		item = itemKey.get()
		# Send the template to the details.html page	
                template_values = {
			'greeting': 'Details for: '+item.title,
			'button1': 'Safe',
			'button2': 'Suspicious',
			'button3': 'New',
			'button4': 'Return to Results',
			'url1': None,
			'url2': None,
			'url3': None,
			'url4': None,
			'projectKey': projectKey,
			'page': page,
			'searchItem': item
		}
		template = JINJA_ENVIRONMENT.get_template('www/details.html')
                self.response.write(template.render(template_values))
