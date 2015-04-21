__author__ = 'brendan'

import os
import os.path
import logging
import uuid
import hashlib
import sys
import json

from webapp2_extras.appengine.auth.models import UserToken
from webapp2_extras.auth import InvalidAuthIdError
from webapp2_extras.auth import InvalidPasswordError
from webapp2_extras import security
from google.appengine.ext import ndb

from models import User
from basehandlers import BaseHandler

#sys.path.insert(0, 'stripe')
#import stripe


# Decorators

def user_required(handler):
    """
        Decorator that checks if there's a user associated with
        the current session. Will also fail if there's no
        session available.
    """

    def check_login(self, *args, **kwargs):
        self.response.headers['Content-Type'] = "application/json"
        user_id = self.request.get('user_id')
        token = self.request.get('token')

        # Does the user id and token exist in the datastore
        response_tuple = User.get_by_auth_token(int(user_id), token)

        # Response is a None tuple then the user id & token do not exist
        if response_tuple == (None, None):
            self.send_response(self.RESPONSE_CODE_401,
                               "User not authenticated",
                               "")
        else:
            return handler(self, *args, **kwargs)

    return check_login


# Helpers

def json_response(error_code, status, response_msg, json_object):
    """
      Global function used to structure JSON output
    """
    output = {'code': error_code,
              'status': status,
              'message': response_msg,
              'response': json_object}

    return json.dumps(output)


class SignupHandler(BaseHandler):
    """Signup New User"""

    def post(self):
        #self.response.headers['Access-Control-Allow-Origin'] = 'https://sandboxx.herokuapp.com'
        #  TODO: Change in basehandlers.py
        #self.response.headers['Access-Control-Allow-Origin'] = 'http://localhost:9000'
        self.response.headers['Content-Type'] = "application/json"

        # Does e-mail already exist?
        jsn = json.loads(self.request.body)
        email = jsn['email']
        password = jsn['password']
        first_name = jsn['first_name']
        last_name = jsn['last_name']
        phone = jsn['phone']

        query = User.query(User.email == email)
        users = query.fetch()

        if users:
            msg = 'Unable to create user.  Duplicate email: %s' % email
            self.send_response(self.RESPONSE_CODE_400, msg, "")
            return

        '''# Create Stripe customer
        stripe.api_key = constants.get_stripe_api_key()
        stripe_customer = stripe.Customer.create()
        stripe_customer_id = stripe_customer.id

        # If stripe customer Id doesn't exist, set to None
        if not stripe_customer_id:
            stripe_customer_id = None
        '''



        # Create a user
        unique_properties = ['email']
        user_data = self.user_model.create_user(email,
                                                unique_properties,
                                                email=email,
                                                password_raw=password,
                                                first_name=first_name,
                                                last_name=last_name,
                                                phone=phone)

                                                #stripeCustomerId=stripe_customer_id

        # If user was not created, probably a duplicate email
        if not user_data[0]:  # user_data is a tuple
            msg = 'Unable to create user.  Duplicate email: %s' % email
            self.send_response(self.RESPONSE_CODE_400, msg, "")
            return

        # New user created.  Get user at index 1
        user = user_data[1]

        user_dict = user.to_dict()

        user_id = user.get_id()
        token = UserToken.create(user_id, subject='auth', token=None)

        user_dict['token'] = str(token.token)
        user_dict['email'] = email

        del user_dict['created']
        del user_dict['joined']
        del user_dict['updated']
        print user_dict


        self.send_response(self.RESPONSE_CODE_200, "User Signed Up", user_dict)


class LoginHandler(BaseHandler):
    """Authenticate new users"""

    def post(self):
        #self.response.headers['Access-Control-Allow-Origin'] = 'https://sandboxx.herokuapp.com'
        #  TODO: Change in basehandlers.py
        #self.response.headers['Access-Control-Allow-Origin'] = 'http://localhost:9000'
        self.response.headers['Content-Type'] = "application/json"

        jsn = json.loads(self.request.body)
        email = jsn['email']
        password = jsn['password']

        # Login with email and password
        try:
            u = self.auth.get_user_by_password(email,
                                               password,
                                               remember=True,
                                               save_session=True)

            query = User.query(User.email == email)
            users = query.fetch()
            user = users[0]
            '''
            # Create Stripe customerID if one doesn't exist
            if not user.stripeCustomerId:
                stripe.api_key = stripe.api_key
                stripe_customer = stripe.Customer.create()
                stripe_customer_id = stripe_customer.id
                user.stripeCustomerId = stripe_customer_id
                user.put()
            '''
            # Merge both objects: auth user object and custom user model
            user_dict = user.to_dict()
            del user_dict['created']
            del user_dict['joined']
            del user_dict['updated']
            results = dict(u.items() + user_dict.items())

            results['email'] = email
            print(results)
            self.send_response(self.RESPONSE_CODE_200, "", results)

        except (InvalidAuthIdError, InvalidPasswordError) as e:
            error_message = 'Login failed for user %s' % email
            self.send_response(self.RESPONSE_CODE_400, error_message, "")


class LogoutHandler(BaseHandler):
    """Logout users"""

    @user_required
    def post(self):
        self.response.headers['Content-Type'] = "application/json"

        jsn = json.loads(self.request.body)
        token = jsn['token']
        user_id = jsn['user_id']

        # Reset current user's device token
        user = User.get_by_auth_token(int(user_id), token)
        user = user[0]
        user.deviceToken = None
        user.put()

        self.user_model.delete_auth_token(user_id, token)
        self.send_response(self.RESPONSE_CODE_200, "User logged out", "")