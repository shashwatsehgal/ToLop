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

        sku = ndb.IntegerProperty()
        dateOfTheft = ndb.DateTimeProperty(auto_now_add=True)
        listPrice = ndb.IntegerProperty()
        zipCode = ndb.IntegerProperty()
        website = ndb.StringProperty()
        status = ndb.StringProperty()

        platforms = [
                SearchPlatform(
                    name = 'eBay',
                    search = False),
                SearchPlatform(
                    name = 'Craigslist',
                    search = False)
        ]
# [END Project]

def stringToKey(projectKey):
        className, idparentheses = projectKey.split(", ")
        id, parentheses = idparentheses.split(")")
        return ndb.Key('Project', int(id))
