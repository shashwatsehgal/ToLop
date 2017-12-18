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
from scoreComputer import ScoreComputer

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
    
    # Generates details of a seller selling am item marked as suspicious
    def getSellerInfo(self, searchResult):
	sellerObj = WatchedSeller()
	sellerObj.userName = searchResult.seller
	sellerObj.url = "https://www.ebay.com/usr/"+searchResult.seller
#	sellerObj.watchedResult = 
    	return sellerObj
	    
    # Saves search results in Datastore. Parameters are newKey (key of the project) and searchResults (output for Finding API call) 
    def saveResults(self, newKey, searchResults):
        for item in searchResults:
            # Search result is stored as an entity with the project entity as the parent
            saveResult = SearchResult(parent = newKey)
            
            # Building the parameters from the Finding API call output
            saveResult.platform = 'eBay'
            saveResult.website = item.viewItemURL
            saveResult.location = item.location
            if hasattr(item, 'postalCode'):
                saveResult.zipCode = item.postalCode
                saveResult.distance = float(item.distance.value)
            else:
                saveResult.zipCode = "0"
                saveResult.distance = 999999
            saveResult.price = float(item.sellingStatus.currentPrice.value)
            if item.shippingInfo.shippingServiceCost == None:
                saveResult.shippingCost = 0
            elif item.shippingInfo.shippingServiceCost == "":
                    saveResult.shippingCost = 0
            else:        
                saveResult.shippingCost = float(item.shippingInfo.shippingServiceCost.value)
            saveResult.shippingTime = int(item.shippingInfo.handlingTime)
            saveResult.condition = item.condition.conditionDisplayName
            saveResult.title = item.title
            if hasattr(item, 'sellerInfo'):
                saveResult.seller = item.sellerInfo.sellerUserName
                saveResult.sellerRating = item.sellerInfo.feedbackScore
            saveResult.postDate = item.listingInfo.startTime
            
            saveResult.comments = ''
            #saveResult.image = ndb.BlobProperty()
            saveResult.imageLink = item.galleryURL
            saveResult.searchStatus = "New"
            saveResult.searchScore = self.__scorer.getScore(saveResult)
            
            # Writing to the Datastore
            saveResult.put()
            
    def get(self):
        # Gets the current user details and checks whether the user has logged in or not
	user = users.get_current_user()
	if user:
	    # User has logged in correctly
	    strKey = self.request.get('id')
	    currentPage = self.request.get('page')
	    newKey = stringToKey(strKey, 'Project')
	    # This parameter can be changed as needed
	    resultsPerPage = 10

	    existingProject = newKey.get()
	    self.__scorer = ScoreComputer(existingProject.listPrice)
	    if existingProject.status == "New":
		api = finding(siteid ='EBAY-US', appid='Shashwat-ToLoP-PRD-35d80d3bd-64e84449', config_file=None)
		api.execute('findItemsAdvanced', {
		    'keywords': ['toys r us ' + existingProject.projectName],
		    'buyerPostalCode': existingProject.zipCode,
		    'itemFilter': [
			{'name': 'ListedIn', 'value': 'EBAY-US'},
			{'name': 'LocatedIn', 'value': 'US'},
			{'name': 'Condition', 'value': 'New'},
			{'name': 'MaxDistance', 'value': '100'}
		    ],
		    'sortOrder': 'DistanceNearest',
		    'outputSelector': 'SellerInfo'
		})
		
		# Check if there is at least 1 result on eBay
		# if hasattr(api.response.reply, 'paginationOutput'):
		if (int(api.response.reply.paginationOutput.totalEntries) > 0):
		    numResults = api.response.reply.paginationOutput.totalEntries
		    numPages = (int(numResults) - int(numResults) % resultsPerPage)//resultsPerPage+ 1 
		    dictstr = api.response.reply.searchResult
		    # Save the results in Datastore
		    self.saveResults(newKey, dictstr.item)
		    
		    # Update the status of the project and write it to the Datastore
		    existingProject.status = "In Progress"
		    existingProject.put()

		    # Create the template for the results.html page
		    searchQuery = SearchResult.query(ancestor =
			    newKey).order(SearchResult.distance)
		    searchResults = list(searchQuery.fetch())
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
			'searchResults': searchResults
		    }
		else:
		    # There are no results on eBay
		    # Create the template for the results.html page
		    template_values = {
			'numResults': 0,
			'numPages': 0,
			'projectID': strKey,
			'currentPage': currentPage,
			'resultsPerPage': resultsPerPage,
			'greeting': 'Results: 0 posts found on eBay',
			'url2': ('/dashboard'),
			'button1': 'Save Results',
			'button2': 'Return to Dashboard',
			'searchResults': None 
		    }
	    # Else the project has already been created before; We will simply load the results from Datastore
	    else:
		searchQuery = SearchResult.query(ancestor =
			newKey).order(SearchResult.distance)
		searchResults = list(searchQuery.fetch())
		numResults = 0
		for item in searchResults:
		    numResults = numResults + 1
		    print(item.searchScore)
		numPages = (int(numResults) - int(numResults) % resultsPerPage)//resultsPerPage+ 1 
		template_values = {
		    'numResults': numResults,
		    'numPages': numPages,
		    'projectID': strKey,
		    'currentPage': currentPage,
		    'resultsPerPage': resultsPerPage,
		    'greeting': "Results: %d posts found on eBay"%numResults,
		    'url2': ('/dashboard'),
		    'button1': 'Save Results',
		    'button2': 'Return to Dashboard',
		    'searchResults': searchResults,
		    'comments': existingProject.comments
		}

	    # Send the template to the results.html page    
	    JINJA_ENVIRONMENT.filters['urlencode'] = urlencode
	    template = JINJA_ENVIRONMENT.get_template('www/results.html')
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
        if strItemKey != None:
            itemKey = stringToKeyWithParent(strItemKey, 'Project', 'SearchResult')
        if self.request.POST.get('safe', None):
            existingItem = itemKey.get()
            existingItem.searchStatus = "Safe"
            existingItem.put()
            self.redirect('/run?id='+strKey+'&page='+page)
        elif self.request.POST.get('suspicious', None):
            existingItem = itemKey.get()
            existingItem.searchStatus = "Suspicious"
            existingItem.put()
	    suspiciousSeller = getSellerInfo(existingItem)
	    suspiciousSeller.put()
            self.redirect('/run?id='+strKey+'&page='+page)
        elif self.request.POST.get('details', None):
            self.redirect('/details?id='+strKey+'&page='+page+'&item='+strItemKey)
        elif self.request.POST.get('newComment', None):
            existingProject = projectKey.get()
            existingProject.comments = existingProject.comments + '\nOn '+datetime.now().strftime("%Y-%m-%d")+', '+users.get_current_user().nickname()+" wrote: "+self.request.POST.get('newComment',None)+'\n--------------------------------------------------------------------------------\n'
            existingProject.put()
            self.redirect('/run?id='+strKey+'&page='+page)
