# [START imports]
import os
import urllib


import ebaysdk
from ebaysdk.finding import Connection as finding

# [START RunProject]
api = finding(appid='Shashwat-ToLoP-PRD-35d80d3bd-64e84449', config_file=None)
api.execute('findItemsAdvanced', {
	'keywords': ['toys r us','exclusive'],
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

