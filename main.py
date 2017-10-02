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

from login import LoginPage
from dashboard import Dashboard
from createProject import CreateProject
from runProject import RunProject

# [START app]
app = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/dashboard', Dashboard),
    ('/create', CreateProject),
    ('/run', RunProject),
], debug=True)
# [END app]

