
# [START imports]
import os
import urllib

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


# [START greeting]
class Author(ndb.Model):
    """Sub model for representing an author."""
    identity = ndb.StringProperty(indexed=False)
    email = ndb.StringProperty(indexed=False)


class Project(ndb.Model):
    """A main model for representing an individual Project entry."""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
# [END greeting]


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
#	    self.response.write("<html><a href = {}>Dashboard </a></html>".format(next_url1))
#	    self.response.write("<html><a href = {}>Sign Out </a></html>".format(next_url2))
        else:
            next_url1 = users.create_login_url('/dashboard')
	    next_url2 = None
	    greeting = 'You are logged out. Please sign in to proceed'
	    button1 = 'Log in'
	    button2 = None
#	    self.response.write("<html><a href = {}>Sign in </a></html>".format(next_url1))
	template_values = {
	    'greeting': greeting,
	    'url1': next_url1,
	    'url2': next_url2,
	    'button1': button1,
	    'button2': button2
	}
	print(template_values)
	template = JINJA_ENVIRONMENT.get_template('www/index.html')
	self.response.write(template.render(template_values))

	
# [END LoginPage]


# [START CreateProject]
class CreateProject(webapp2.RequestHandler):
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
	    self.response.write('<html>This is a dashboard</html>')
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
