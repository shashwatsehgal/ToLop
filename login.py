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
           		if self.request.get('id', None):
        			strKey = self.request.get('id')
				newKey = stringToKey(strKey)
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
			if self.request.POST.get('key'):
				strKey = self.request.POST.get('key')
				newKey = stringToKey(strKey)
				newProject = newKey.get()
			else:
				newProject = Project()
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
				newProject.listPrice = int(self.request.get('listPrice'))
            		if self.request.get('zipCode')=="":
				newProject.zipCode = 0
	    		else:
				newProject.zipCode = int(self.request.get('zipCode'))
            		newProject.website = self.request.get('website')
            		newProject.platforms = self.request.get('platform', allow_multiple=True)
            		newProject.status = "In Progress"
	    		newProject.put()
	    		self.redirect('/dashboard')
		elif self.request.POST.get('return', None):
	    		key = self.redirect('/dashboard')
# [END CreateProject]


# [START Dashboard]
class Dashboard(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        if user:
            project_query = Project.query()
            projects = project_query.fetch(10)
            template_values = {
                'greeting': 'Dashboard',
                'url1': ('/create'),
                'url2': users.create_logout_url('/'),
                'button1': 'New Project',
                'button2': 'Logout',
                'projects': projects
                }
            template = JINJA_ENVIRONMENT.get_template('www/dashboard.html')
            self.response.write(template.render(template_values))

        else:
            template_values = {
                'greeting': 'You are logged out. Please sign in to proceed',
                'url1': users.create_login_url('/dashboard'),
                'button1': 'Login',
                'button2': None
                }
            template = JINJA_ENVIRONMENT.get_template('www/index.html')
            self.response.write(template.render(template_values))

    def post(self):
        strKey = self.request.get('key')
	newKey = stringToKey(strKey)
	if self.request.POST.get('delete', None):
	    newKey.delete()
	    self.redirect('/dashboard')
	elif self.request.POST.get('edit', None):
	    self.redirect('/create?id='+strKey) 
 
# [End Dashboard]


# [START app]
app = webapp2.WSGIApplication([
    ('/', LoginPage),
    ('/dashboard', Dashboard),
    ('/create', CreateProject),
], debug=True)
# [END app]
