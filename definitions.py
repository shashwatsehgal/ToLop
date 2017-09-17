# [START imports]
import os
import urllib

from datetime import datetime
from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

import dashboard


JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

DEFAULT_PROJECT_NAME = 'default_project'


# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

def project_key(project_name=DEFAULT_PROJECT_NAME):
    """Constructs a Datastore key for a Project entity.
    We use project_name as the key.
    """
    return ndb.Key('Project', project_name)

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

