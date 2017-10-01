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

# [START RunProject]
class RunProject(webapp2.RequestHandler):
	def get(self):
		strKey = self.request.get('id')
		newKey = stringToKey(strKey)
		existingProject = newKey.get()
		api = finding(siteid ='EBAY-US', appid='Shashwat-ToLoP-PRD-35d80d3bd-64e84449', config_file=None)
		api.execute('findItemsAdvanced', {
			'keywords': ['toys r us exclusive '+existingProject.projectName],
			'buyerPostalCode': existingProject.zipCode,
			'itemFilter': [
        			{'name': 'ListedIn', 'value': 'EBAY-US'},
        			{'name': 'LocatedIn', 'value': 'US'},
        			{'name': 'Condition', 'value': 'New'},
        			{'name': 'MinPrice', 'value': '100', 'paramName': 'Currency', 'paramValue': 'USD'},
        			{'name': 'MaxPrice', 'value': '10000', 'paramName': 'Currency', 'paramValue': 'USD'},
				{'name': 'MaxDistance', 'value': '100'}
    			],
    			'sortOrder': 'DistanceNearest'
		})
 	
		if hasattr(api.response.reply, 'paginationOutput'):
			numResults = api.response.reply.paginationOutput.totalEntries
			numPages = (int(numResults) - int(numResults) % 50)//50 + 1 
			dictstr = api.response.reply.searchResult
			template_values = {
				'numResults': numResults,
				'numPages': numPages,
				'projectID': strKey,
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
				'greeting': 'Results: 0 posts found on eBay',
                        	'url2': ('/dashboard'),
     	        	        'button1': 'Save Results',
        	                'button2': 'Return to Dashboard'
			}
                template = JINJA_ENVIRONMENT.get_template('www/results.html')
                self.response.write(template.render(template_values))		
	
#		for i in dictstr.item:
#    			print "Title: %s" % i.title
#    			print "URL: %s" % i.viewItemURL
#    			print "ZIP Code: %s" % i.postalCode
#    			print "Location: %s" % i.location
#    			print "Price: $%s" % i.sellingStatus.currentPrice.value
#    			print "Condition: %s" % i.condition.conditionDisplayName
#    			print "Post Time: %s" % i.listingInfo.startTime
#    			if hasattr(i.shippingInfo, 'shippingServiceCost'): 
#    				print "Shipping Cost: $%s" % i.shippingInfo.shippingServiceCost.value 
#    			else: 
#    				print "Shipping Cost: $0"
#	print "\n"

