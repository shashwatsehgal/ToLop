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
from authModel import *
from authBaseCode import *

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
class RunProject(BaseHandler):
    # Generates details of a seller selling am item marked as suspicious
    def getSellerInfo(self, searchResult):
	sellerObj = WatchedSeller()
	sellerObj.userName = searchResult.seller
	sellerObj.url = "https://www.ebay.com/usr/"+searchResult.seller
	sellerObj.watchedResultTitle = searchResult.title 
	sellerObj.watchedResultURL = searchResult.website
	sellerObj.sellerRating = searchResult.sellerRating
    	sellerObj.timesFlagged = 1
	api = finding(siteid ='EBAY-US', appid='Shashwat-ToLoP-PRD-35d80d3bd-64e84449', config_file=None)
	api.execute('findItemsAdvanced', {
	    'keywords': ['toys r us'],
	    'itemFilter': [
		{'name': 'ListedIn', 'value': 'EBAY-US'},
		{'name': 'LocatedIn', 'value': 'US'},
		{'name': 'Seller', 'value': searchResult.seller}
	    ],
	    'sortOrder': 'EndTimeSoonest',
	    'outputSelector': 'SellerInfo'
	})
	sellerObj.numberOfPosts = int(api.response.reply.paginationOutput.totalEntries)
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
                saveResult.sellerRating = float(item.sellerInfo.positiveFeedbackPercent)
            saveResult.postDate = item.listingInfo.startTime
            saveResult.comments = ''
            #saveResult.image = ndb.BlobProperty()
            saveResult.imageLink = item.galleryURL
            saveResult.searchStatus = "New"
            saveResult.searchScore = self.__scorer.getScore(saveResult)
            
            # Writing to the Datastore
            saveResult.put()
            
    @user_required
    def get(self):
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
		'keywords': [self.user.company + ' ' + existingProject.projectName],
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
		numPages = (int(numResults) - int(numResults) % resultsPerPage)//resultsPerPage
		if int(numResults) % resultsPerPage > 0:
		    numPages = numPages + 1
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
		    'company': self.user.company,
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
		    'company': self.user.company,
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
	    numPages = (int(numResults) - int(numResults) % resultsPerPage)//resultsPerPage 
	    if int(numResults) % resultsPerPage > 0:
	        numPages = numPages + 1
	    
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
		'company': self.user.company,
		'comments': existingProject.comments
	    }

	# Send the template to the results.html page    
	JINJA_ENVIRONMENT.filters['urlencode'] = urlencode
	template = JINJA_ENVIRONMENT.get_template('www/results.html')
	self.response.write(template.render(template_values))

    def post(self):
        strKey = self.request.get('projectKey')
        projectKey = stringToKey(strKey, 'Project')
        page = self.request.get('page')
        strItemKey = self.request.get('itemKey')
	if strItemKey != "":
            itemKey = stringToKeyWithParent(strItemKey, 'Project', 'SearchResult')
        # If-else loop for how the user interacts with the results
	if self.request.POST.get('safe', None):
	    # User marks a result as safe
            existingItem = itemKey.get()
            existingItem.searchStatus = "Safe"
            existingItem.put()
            # Remove the seller from the Suspicious Seller List
	    # Check if the seller is in the suspicious seller list. If yes, then decrease the number of suspicious posts by 1
	    searchQuery = WatchedSeller.query(WatchedSeller.userName == existingItem.seller)
	    for s in searchQuery:
		s.timesFlagged = s.timesFlagged - 1
		if s.timesFlagged == 0:
		    s.key.delete()
		else:
		    s.put() 
	    self.redirect('/run?id='+strKey+'&page='+page)
        elif self.request.POST.get('suspicious', None):
            # User marks a result as suspicious
	    existingItem = itemKey.get()
            if existingItem.searchStatus != "Suspicious":
		    existingItem.searchStatus = "Suspicious"
		    existingItem.put()
		    # Add the seller to the Suspicious Seller List
		    # Check if the seller is already in the suspicious seller list. If yes, then increase the number of suspicious posts by that seller by 1
		    searchQuery = WatchedSeller.query(WatchedSeller.userName == existingItem.seller)
		    isSellerInList = 0
		    for s in searchQuery:
			isSellerInList = isSellerInList + 1
			s.timesFlagged = s.timesFlagged + 1
			s.put() 
		    # If seller is not in the suspicious list, add to the list
		    if isSellerInList == 0:
			suspiciousSeller = self.getSellerInfo(existingItem)
			suspiciousSeller.put()
	    self.redirect('/run?id='+strKey+'&page='+page)
        elif self.request.POST.get('details', None):
            self.redirect('/details?id='+strKey+'&page='+page+'&item='+strItemKey)
        elif self.request.POST.get('newComment', None):
            existingProject = projectKey.get()
            existingProject.comments = existingProject.comments + '\nOn '+datetime.now().strftime("%Y-%m-%d")+', '+self.user.name+ " "+ self.user.last_name+" wrote: "+self.request.POST.get('newComment',None)+'\n--------------------------------------------------------------------------------\n'
            existingProject.put()
            self.redirect('/run?id='+strKey+'&page='+page)
