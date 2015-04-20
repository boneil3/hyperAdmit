import webapp2
import json
import os
import os.path
from google.appengine.ext.webapp import template
from google.appengine.ext import deferred

from webapp2_extras import sessions
from webapp2_extras import auth


# Base Handler Class

class BaseHandler(webapp2.RequestHandler):
    RESPONSE_CODE_200 = 200
    RESPONSE_CODE_400 = 400
    RESPONSE_CODE_401 = 401

    @webapp2.cached_property
    def auth(self):
        """Shortcut to access the auth instance as a property."""
        return auth.get_auth()

    @webapp2.cached_property
    def user_info(self):
        """Shortcut to access a subset of the user attributes that are stored
        in the session.

        The list of attributes to store in the session is specified in
          config['webapp2_extras.auth']['user_attributes'].
        :returns
          A dictionary with most user information
        """
        return self.auth.get_user_by_session()

    @webapp2.cached_property
    def user(self):
        """Shortcut to access the current logged in user.

        Unlike user_info, it fetches information from the persistence layer and
        returns an instance of the underlying model.

        :returns
          The instance of the user model associated to the logged in user.
        """
        u = self.user_info
        return self.user_model.get_by_id(u['user_id']) if u else None

    @webapp2.cached_property
    def user_model(self):
        """Returns the implementation of the user model.

        It is consistent with config['webapp2_extras.auth']['user_model'], if set.
        """
        return self.auth.store.user_model

    @webapp2.cached_property
    def session(self):
        """Shortcut to access the current session."""
        return self.session_store.get_session(backend="datastore")

    def render_template(self, view_filename, params={}):
        user = self.user_info
        params['user'] = user
        path = os.path.join(os.path.dirname(__file__), 'views', view_filename)
        self.response.out.write(template.render(path, params))

    def display_message(self, message):
        """Utility function to display a template with a simple message."""
        params = {
            'message': message
        }
        self.render_template('message.html', params)

    # this is needed for webapp2 sessions to work
    def dispatch(self):
        # Get a session store for this request.
        self.session_store = sessions.get_store(request=self.request)

        try:
            # Dispatch the request.
            webapp2.RequestHandler.dispatch(self)
        finally:
            # Save all sessions.
            self.session_store.save_sessions(self.response)

    def send_response(self, response_code, response_msg, json_object):
        """Function used to send JSON response"""

        status = ""
        if response_code == self.RESPONSE_CODE_200:
            status = "success"
        elif response_code == self.RESPONSE_CODE_400:
            status = "error"

        output = {'code': response_code,
                  'status': status,
                  'message': response_msg,
                  'response': json_object}
        json_dict = json.dumps(output)
        self.response.write(json_dict)

    def options(self):
        #self.response.headers['Access-Control-Allow-Origin'] = 'https://sandboxx.herokuapp.com'
        #self.response.headers['Access-Control-Allow-Origin'] = 'http://localhost:9000'
        self.response.headers['Access-Control-Allow-Headers'] = 'Origin, X-Requested-With, Content-Type, Accept'
        self.response.headers['Access-Control-Allow-Methods'] = 'POST, GET, PUT, DELETE'
        self.response.headers['Content-Type'] = "application/json"
