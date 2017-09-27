# [START imports]
import os
import urllib

from datetime import datetime
from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from baseClasses import *
from createProject import *
from runProject import *
from dashboard import *
from login import *

# [START app]
app = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/dashboard', Dashboard),
    ('/create', CreateProject),
    ('/run', RunProject),
], debug=True)
# [END app]


