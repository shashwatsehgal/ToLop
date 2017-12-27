# [START imports]
import os
import urllib

from datetime import datetime
from google.appengine.api import users
from google.appengine.ext import ndb
from google.appengine.api import mail

import jinja2
import webapp2

from baseClasses import *
from authModel import *
from authBaseCode import *

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
    	autoescape=True)
# [END imports]
    
# [START LoginPage]
class LoginPage(BaseHandler):
	def get(self):
    		self._serve_page()

  	def post(self):
    		username = self.request.get('username')
    		password = self.request.get('password')
    		try:
      			u = self.auth.get_user_by_password(username, password, remember=True,
        		save_session=True)
      			self.redirect('/dashboard')
    		except (InvalidAuthIdError, InvalidPasswordError) as e:
      			logging.info('Login failed for user %s because of %s', username, type(e))
      			self._serve_page(True)

  	def _serve_page(self, failed=False):
    		username = self.request.get('username')
    		params = {
      			'username': username,
      			'failed': failed,
    		}
		template = JINJA_ENVIRONMENT.get_template('www/index.html')
		self.response.write(template.render(params))
# [END LoginPage]

# [START LogoutPage]
class LogoutPage(BaseHandler):
	def get(self):
		self.auth.unset_session()
	        self.redirect('/')
# [END LogoutPage]

# [START UserProfile]
class UserProfile(BaseHandler):
	@user_required
	def get(self):
		params = {
			'user': self.user,
			'greeting': ""
		}
		template = JINJA_ENVIRONMENT.get_template('www/profile.html')
		self.response.write(template.render(params))

	@user_required
	def post(self):
	    	password = self.request.get('password')
	    	old_token = self.request.get('t')

	    	if not password or password != self.request.get('confirm_password'):
	      		greeting = 'ERROR: Passwords do not match!'
	      	
		else:
		    	user = self.user
		    	user.set_password(password)
	    		user.put()
		    	# remove signup token, we don't want users to come back with an old link
		    	self.user_model.delete_signup_token(user.get_id(), old_token)
	    		greeting = 'Password updated successfully!'
		
		params = {
                        'user': self.user,
			'message': greeting	
                }
                template = JINJA_ENVIRONMENT.get_template('www/profile.html')
                self.response.write(template.render(params))
# [END UserProfile]

# [START ForgotPassword]
class ForgotPassword(BaseHandler):
 	def get(self):
    		self._serve_page(email_sent=False)

  	def post(self):
    		username = self.request.get('username')

    		user = self.user_model.get_by_auth_id(username)
    		if not user:
      			logging.info('Could not find any user entry for username %s', username)
      			self._serve_page(not_found=True, email_sent=False)
      			return

    		user_id = user.get_id()
    		token = self.user_model.create_signup_token(user_id)

    		# verification_url = self.uri_for('verification', type='p', user_id=user_id,
      		#	signup_token=token, _full=True)

    		# msg = 'Send an email to user in order to reset their password. \
          	#	They will be able to do so by visiting <a href="{url}">{url}</a>'

    		# self.display_message(msg.format(url=verification_url))
		mail.send_mail(sender='shashwatsehgal@gmail.com',
                	to=user.email_address,
                   	subject="Password Reset",
                   	body="Please click here to reset your password: +verification_url+\n\nThe DEFENCE.com Team")	
		self._serve_page()

  	def _serve_page(self, not_found=False, email_sent=True):
    		username = self.request.get('username')
   		params = {
   		 	'username': username,
   			'not_found': not_found,
			'email_sent': email_sent
    		}
		template = JINJA_ENVIRONMENT.get_template('www/forgot.html')
                self.response.write(template.render(params))
# [END ForgotPassiword]
