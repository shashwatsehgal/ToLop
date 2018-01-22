# [START imports]
import os
import urllib

from datetime import datetime
from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

from baseClasses import *

JINJA_ENVIRONMENT = jinja2.Environment(
        loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
        extensions=['jinja2.ext.autoescape'],
        autoescape=True)
# [END imports]


# [START CreateProject]
class CreateProject(webapp2.RequestHandler):
        def get(self):
                # Gets the current user details and checks whether the user has logged in or not
		user = users.get_current_user()
		if user:
			# User has logged in correctly
			# Checks whether the user is creating a new project or opening an existing project
                        if self.request.get('id', None):
				# Loads an existing project
                                strKey = self.request.get('id')
                                newKey = stringToKey(strKey, 'Project')
                                existingProject = newKey.get()
                                template_values = {
                                        'greeting': 'Edit Project',
                                        'projectName': existingProject.projectName,
                                        'author': existingProject.author,
                                        'date': existingProject.date.strftime("%m/%d/%Y"),
                                        'sku': existingProject.sku,
                                        'dateOfTheft': existingProject.dateOfTheft.strftime("%m/%d/%Y"),
                                        'listPrice': existingProject.listPrice,
                                        'zipCode': existingProject.zipCode,
                                        'website': existingProject.website,
                                        'status': existingProject.status,
                                        'strKey': strKey
                                }
                        else:
                                # Creates a new project
				nickname = user.nickname()
                                greeting = 'Create New Project'
                                template_values = {
                                        'greeting': greeting,
                                        'author': nickname,
                                        'date': datetime.today().strftime('%m/%d/%Y')
                                }
                        template = JINJA_ENVIRONMENT.get_template('www/create.html')
                        self.response.write(template.render(template_values))
                else:
                        # Not logged in. Redirects to login page
			template_values = {
                                'greeting': 'You are logged out. Please sign in to proceed',
                                'url1': users.create_login_url('/dashboard'),
                                'button1': 'Login',
                                'button2': None,
                        }
                        template = JINJA_ENVIRONMENT.get_template('www/index.html')
                        self.response.write(template.render(template_values))


        def post(self):
                if self.request.POST.get('save', None):
                        # Checks whether the user is creating a new project or opening an existing project
			if self.request.POST.get('key'):
				# Existing project
                                strKey = self.request.POST.get('key')
                                newKey = stringToKey(strKey, 'Project')
                                newProject = newKey.get()
                        else:
				# New project
                                newProject = Project()
                        	newProject.status = "New"
                        
			# Saves down all the attributes of the new/existing project
			newProject.projectName = self.request.get('projectName')
                        newProject.author = self.request.get('author')
                        newProject.date = datetime.strptime(self.request.get('date'),"%m/%d/%Y")
                        if self.request.get('sku')=="":
                                newProject.sku = 0
                        else:
                                newProject.sku = int(self.request.get('sku'))
                        newProject.dateOfTheft = datetime.strptime(self.request.get('dateOfTheft'),"%m/%d/%Y")
                        if self.request.get('listPrice')=="":
                                newProject.listPrice = 0
                        else:
                                newProject.listPrice = float(self.request.get('listPrice'))
                        if self.request.get('zipCode')=="":
                                newProject.zipCode = "0"
                        else:
                                newProject.zipCode = self.request.get('zipCode')
                        newProject.website = self.request.get('website')
                        newProject.platforms = self.request.get('platform', allow_multiple=True)
			newProject.comments = ''
			
			# Saves the project in the datastore and redirects to the dashboard
			newProject.put()
                        self.redirect('/dashboard')
                elif self.request.POST.get('return', None):
                        # Does not make any changes and returns to the dashboard
			key = self.redirect('/dashboard')
# [END CreateProject]
