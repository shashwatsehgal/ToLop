# [START imports]
import os
import urllib

from datetime import datetime
from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2


JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True)
# [END imports]

# [START SearchResult]
class SearchResult(ndb.Model):
	platform = ndb.StringProperty()
	zipCode = ndb.StringProperty()
	distance = ndb.FloatProperty()
	website = ndb.StringProperty()
	price = ndb.FloatProperty()
	shippingCost = ndb.FloatProperty()
	shippingTime = ndb.IntegerProperty()
	condition = ndb.StringProperty()
	title = ndb.StringProperty()
	seller = ndb.StringProperty()
	sellerRating = ndb.FloatProperty()
	location = ndb.StringProperty()
	postDate = ndb.DateProperty()
	comments = ndb.TextProperty()
	image = ndb.BlobProperty()
	imageLink = ndb.StringProperty()	
	searchStatus = ndb.StringProperty()
	searchScore = ndb.FloatProperty()
# [END SearchResult]

# [START WatchedSeller]
class WatchedSeller(ndb.Model):
	userName = ndb.StringProperty()
	url = ndb.StringProperty()
	watchedResultTitle = ndb.StringProperty()
	watchedResultURL = ndb.StringProperty()
	sellerRating = ndb.FloatProperty()
	timesFlagged = ndb.IntegerProperty()
	numberOfPosts = ndb.IntegerProperty()
	result1 = SearchResult()
	result2 = SearchResult()
	result3 = SearchResult()
	result4 = SearchResult()
	result5 = SearchResult()
# [END WatchedSeller]

# [START SearchPlatform]
class SearchPlatform(ndb.Model):
        name = ndb.StringProperty()
        url = ndb.StringProperty()
        search = ndb.BooleanProperty()
# [END SearchPlatform]

# [START Project]
class Project(ndb.Model):
        """A main model for representing an individual Project entry."""
        projectName = ndb.StringProperty(indexed=False)
        author = ndb.StringProperty(indexed=False)
        date = ndb.DateTimeProperty(auto_now_add=True)
	company = ndb.StringProperty()

        sku = ndb.IntegerProperty()
        dateOfTheft = ndb.DateTimeProperty(auto_now_add=True)
        listPrice = ndb.FloatProperty()
        zipCode = ndb.StringProperty()
        website = ndb.StringProperty()
        status = ndb.StringProperty()
	comments = ndb.TextProperty() 

        platforms = [
                SearchPlatform(
                    name = 'eBay',
                    search = False),
                SearchPlatform(
                    name = 'Craigslist',
                    search = False)
        ]
# [END Project]

def stringToKey(Key, entityName):
        className, idparentheses = Key.split(", ")
        id, parentheses = idparentheses.split(")")
        return ndb.Key(entityName, int(id))

def stringToKeyWithParent(Key, parentName, entityName):
        KeyWord, rest = Key.split("'"+parentName+"', ")
	parentID, entityIDparentheses = rest.split(", '"+entityName+"', ")
        entityID, parentheses = entityIDparentheses.split(")")
        return ndb.Key(entityName, int(entityID), parent = ndb.Key(parentName, int(parentID)))
