__author__ = 'brendan'

import webapp2

from backend.auth import *

config = {
    'webapp2_extras.auth': {
        'user_model': 'backend.models.User',
        'user_attributes': ['email']
    },
    'webapp2_extras.sessions': {
        # TODO: Set before launch
        # Secret key to generate session cookies
        'secret_key': 'GREENWICH'
    }
}


# Application Instance
# Debugging should be set to 'False' for production

application = webapp2.WSGIApplication([


    # AUTHENTICATION
    webapp2.Route('/api/signup', SignupHandler, name='signup'), #API
    webapp2.Route('/api/login', LoginHandler, name='login'), #API
    webapp2.Route('/api/logout', LogoutHandler, name='logout'), #API


], debug=True, config=config)