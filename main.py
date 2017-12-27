# [START imports]
import os
import urllib

from datetime import datetime
from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

import requests_toolbelt.adapters.appengine
requests_toolbelt.adapters.appengine.monkeypatch()

from login import *
from dashboard import Dashboard
from createProject import CreateProject
from runProject import RunProject
from resultDetail import ResultDetail
from newUser import NewUser

config = {
  'webapp2_extras.auth': {
    'user_model': 'authModel.User',
    'user_attributes': ['name']
  },
  'webapp2_extras.sessions': {
    'secret_key': 'YOUR_SECRET_KEY'
  }
}

# [START app]
app = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/logout', LogoutPage),
    ('/profile', UserProfile),
    ('/forgot', ForgotPassword),
    ('/register', NewUser),
    ('/dashboard', Dashboard),
    ('/create', CreateProject),
    ('/run', RunProject),
    ('/details', ResultDetail),
], debug=True, config=config)
# [END app]

