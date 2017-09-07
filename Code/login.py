
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


class Greeting(ndb.Model):
    """A main model for representing an individual Guestbook entry."""
    author = ndb.StructuredProperty(Author)
    content = ndb.StringProperty(indexed=False)
    date = ndb.DateTimeProperty(auto_now_add=True)
# [END greeting]


# [START login]
class Login(webapp2.RequestHandler):

    def get(self):
        #guestbook_name = self.request.get('guestbook_name',
        #                                  DEFAULT_GUESTBOOK_NAME)
        #greetings_query = Greeting.query(
        #    ancestor=guestbook_key(guestbook_name)).order(-Greeting.date)
        #greetings = greetings_query.fetch(10)

        user = users.get_current_user()
        if user:
            nickname = user.nickname()
	    logout_url = users.create_logout_url('www/dashboard.html')
	    greeting = 'Welcome, {}! (<a href = "{}">Sign Out</a>)'.format(nickname, logout_url)
        else:
            login_url = users.create_login_url('/')
	    greeting = '<a href = "{}">Sign In</a>'.format(login_url)

	self.response.write('<html><h1 style="text-align:center">ToLoP - Toyr "R" Us Loss Prevention</h1><body>{}</body></html>'.format(greeting))
# [END Login]


# [START guestbook]
class Guestbook(webapp2.RequestHandler):

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
# [END Guestbook]


# [START app]
app = webapp2.WSGIApplication([
    ('/', Login),
    ('/sign', Guestbook),
], debug=True)
# [END app]
