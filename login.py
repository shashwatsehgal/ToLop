# [START imports]
import os
import urllib
import datetime

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)
# [END imports]

DEFAULT_GUESTBOOK_NAME = 'default_guestbook'


# We set a parent key on the 'Greetings' to ensure that they are all
# in the same entity group. Queries across the single entity group
# will be consistent. However, the write rate should be limited to
# ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
    """Constructs a Datastore key for a Guestbook entity.
    We use guestbook_name as the key.
    """
    return ndb.Key('Guestbook', guestbook_name)

# [START SearchPlatform]
class SearchPlatform(ndb.Model):
    name = ndb.StringProperty()
    url = ndb.StringProperty()
    search = ndb.BooleanProperty()
# [END SearchPlatform]

# [START Project]
class Project(ndb.Model):
    """A main model for representing an individual Project entry."""
    name = ndb.StringProperty(indexed=False)
    author = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)

    sku = ndb.IntegerProperty()
    dateOfTheft = ndb.DateTimeProperty(auto_now_add=True)
    listPrice = ndb.IntegerProperty()
    zipCode = ndb.IntegerProperty()
    website = ndb.StringProperty()

    platforms = [
    	SearchPlatform(
	    name = 'eBay',
	    search = False),
	SearchPlatform(
	    name = 'Craigslist',
	    search = False)
	]
# [END Project]


# [START LoginPage]
class LoginPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
	    next_url1 = '/dashboard'
	    next_url2 = users.create_logout_url('/')
	    greeting = 'Welcome, {}'.format(nickname)
	    button1 = 'Dashboard'
	    button2 = 'Log Out'
        else:
            next_url1 = users.create_login_url('/dashboard')
	    next_url2 = None
	    greeting = 'You are logged out. Please sign in to proceed'
	    button1 = 'Log in'
	    button2 = None
	
	template_values = {
	    'greeting': greeting,
	    'url1': next_url1,
	    'url2': next_url2,
	    'button1': button1,
	    'button2': button2
	}
	
	template = JINJA_ENVIRONMENT.get_template('www/index.html')
	self.response.write(template.render(template_values))

	
# [END LoginPage]


# [START CreateProject]
class CreateProject(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            nickname = user.nickname()
	    greeting = 'Create New Project'
	    button1 = 'Dashboard'
	    button2 = 'Log Out'
        else:
            next_url1 = users.create_login_url('/dashboard')
	    next_url2 = None
	    greeting = 'You are logged out. Please sign in to proceed'
	    button1 = 'Log in'
	    button2 = None
	template_values = {
	    'greeting': greeting,
	    'author': nickname,
	    'date': datetime.datetime.today().strftime('%m-%d-%Y')
	}
	print(template_values)
	template = JINJA_ENVIRONMENT.get_template('www/create.html')
	self.response.write(template.render(template_values))
    
    def post(self):
        guestbook_name = self.request.get('guestbook_name',
                                          DEFAULT_GUESTBOOK_NAME)
        greeting = Greeting(parent=guestbook_key(guestbook_name))
        if users.get_current_user():
            greeting.author = Author(
                    identity=users.get_current_user().user_id(),
                    email=users.get_current_user().email())

        greeting.content = self.request.get('content')
        greeting.put()
        query_params = {'guestbook_name': guestbook_name}
        self.redirect('/?' + urllib.urlencode(query_params))
# [END CreateProject]


# [START Dashboard]
class Dashboard(webapp2.RequestHandler):
    def get(self):
	user = users.get_current_user()
	if user:
	    self.response.write('<html>This is a dashboard. <a href = "/create"> Create project</a></html>')
	else:
	    self.response.write('<html>Invalid Login - pls relogin</html>')
# [End Dashboard]

# [START app]
app = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/dashboard', Dashboard),
    ('/create', CreateProject),
], debug=True)
# [END app]
