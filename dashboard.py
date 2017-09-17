import definitions



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
        if self.request.POST.get('delete', None):
                print("DELETING!!!")
# [End Dashboard]

