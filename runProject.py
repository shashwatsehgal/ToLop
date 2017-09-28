# [START imports]
import ebaysdk
from ebaysdk import finding
from ebaysdk.finding import Connection as finding
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

# [START RunProject]
class RunProject(webapp2.RequestHandler):
	def get(self):
		strKey = self.request.get('id')
		newKey = stringToKey(strKey)
		existingProject = newKey.get()

		api = finding(appid='Shashwat-ToLoP-PRD-35d80d3bd-64e84449', config_file=None)
		api.execute('findItemsAdvanced', {
			'keywords': ['toys r us','exclusive',existingProject.projectName],
			'itemFilter': [
        			{'name': 'Condition', 'value': 'New'},
        			{'name': 'MinPrice', 'value': '1', 'paramName': 'Currency', 'paramValue': 'USD'},
        			{'name': 'MaxPrice', 'value': '10000', 'paramName': 'Currency', 'paramValue': 'USD'}
    			],
    			'paginationInput': {
        			'entriesPerPage': '25',
			        'pageNumber': '1' 	 
			},
    			'sortOrder': 'CurrentPriceHighest'
		})
		
		dictstr = api.response.reply.searchResult
 		
		template_values = {
			'greeting': 'Results',
                        'url2': ('/dashboard'),
                        'button1': 'Save Results',
                        'button2': 'Return to Dashboard',
                        'searchResults': dictstr 
                        }
                template = JINJA_ENVIRONMENT.get_template('www/results.html')
                self.response.write(template.render(template_values))		
	
	
		for i in dictstr.item:
    			print "Title: %s" % i.title
    			print "URL: %s" % i.viewItemURL
    			print "ZIP Code: %s" % i.postalCode
    			print "Location: %s" % i.location
    			print "Price: $%s" % i.sellingStatus.currentPrice.value
    			print "Condition: %s" % i.condition.conditionDisplayName
    			print "Post Time: %s" % i.listingInfo.startTime
    			if hasattr(i.shippingInfo, 'shippingServiceCost'): 
    				print "Shipping Cost: $%s" % i.shippingInfo.shippingServiceCost.value 
    			else: 
    				print "Shipping Cost: $0"
    				print "\n"

