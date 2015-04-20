__author__ = 'Brendan'
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
from endpoints_proto_datastore.ndb.model import EndpointsModel
from endpoints_proto_datastore.ndb.properties import EndpointsAliasProperty
from endpoints_proto_datastore.ndb import EndpointsDateTimeProperty
from endpoints_proto_datastore.ndb import utils
from google.appengine.ext import ndb
import endpoints
import webapp2_extras.appengine.auth.models
from webapp2_extras import security
import time


class Appointments(EndpointsModel):

    start_dt = EndpointsDateTimeProperty(required=True)
    end_dt = EndpointsDateTimeProperty(required=True)
    cancelled = ndb.BooleanProperty(default=False)
    request_user = ndb.KeyProperty(kind='User', required=True)
    admission_officer = ndb.KeyProperty(kind='AdmissionsOfficer', required=True)
    scheduled = EndpointsDateTimeProperty(auto_now_add=True)


class User(EndpointsModel, webapp2_extras.appengine.auth.models.User):
    """ User Base Model """

    joined = EndpointsDateTimeProperty(auto_now=True)
    email = ndb.StringProperty(required=True)
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    phone = ndb.StringProperty(required=True)
    stripeCustId = ndb.StringProperty(default=None)
    alias = ndb.StringProperty(default=None)
    appointments = ndb.KeyProperty(kind='Appointments', default=None, repeated=True)

    def id_setter(self, value):
        # Allocate IDs if DNE
        if value == '' or value is None or value == 'None':
            first, last = User.allocate_ids(2)
            self.UpdateFromKey(ndb.Key('User', int(first)))
        elif not isinstance(value, basestring) and not isinstance(value, int):
            raise endpoints.BadRequestException('ID not string or int')
        else:
            self.UpdateFromKey(ndb.Key('User', int(value)))

    @EndpointsAliasProperty(setter=id_setter, required=True)
    def id(self):
        if self.key is not None:
            return str(self.key.id())

    def set_password(self, raw_password):
        """Sets the password for the current user

        :param raw_password:
        The raw password which will be hashed and stored
        """
        self.password = security.generate_password_hash(raw_password, length=12)

    @classmethod
    def get_by_auth_token(cls, user_id, token, subject='auth'):
        """Returns a user object based on a user ID and token.

        :param user_id:
        The user_id of the requesting user.
        :param token:
        The token string to be verified.
        :returns:
        A tuple ``(User, timestamp)``, with a user object and
        the token timestamp, or ``(None, None)`` if both were not found.
        """
        token_key = cls.token_model.get_key(user_id, subject, token)
        user_key = ndb.Key(cls, user_id)

        # Use get_multi() to save a RPC call.
        valid_token, user = ndb.get_multi([token_key, user_key])

        if valid_token and user:
            timestamp = int(time.mktime(valid_token.created.timetuple()))
            if hasattr(user, 'force_login'):
                user.force_login = False
                user.put()
                return None, None
            else:
                return user, timestamp

        return None, None


class University(EndpointsModel):
    """ University Institution Model """
    UNIV_TYPES = []

    rank = ndb.IntegerProperty(required=True)
    name = ndb.StringProperty(required=True)
    type = ndb.StringProperty(required=True, choices=UNIV_TYPES)
    major = ndb.StringProperty(required=False)


class AdmissionsOfficer(EndpointsModel, webapp2_extras.appengine.auth.models.User):
    """ Admissions Officer Model """

    _message_fields_schema = ('id', 'verified', 'school', 'school_type', 'location', 'rating', 'alias',
                              'hours_consulted',
                              'last_active', 'knowledge_areas', 'whoami', 'job_title', 'howcanihelp', 'college_rank')

    email = ndb.StringProperty(required=True)
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    phone = ndb.StringProperty(required=True)
    stripeCustId = ndb.StringProperty(default=None)
    alias = ndb.StringProperty(default=None)
    appointments = ndb.KeyProperty(kind='Appointments', default=None, repeated=True)
    verified = ndb.BooleanProperty(default=False)
    paymentStuff = ndb.StringProperty(default='')
    school = ndb.StringProperty(default='')
    school_type = ndb.StringProperty(default='')
    location = ndb.StringProperty(default='')
    rating = ndb.FloatProperty(default=5.0)
    hours_consulted = ndb.IntegerProperty(default=0)
    last_active = EndpointsDateTimeProperty(auto_now=True)
    knowledge_areas = ndb.StringProperty(repeated=True)
    whoami = ndb.StringProperty(default='')
    howcanihelp = ndb.StringProperty(default='')
    job_title = ndb.StringProperty(default='')
    college_rank = ndb.StringProperty(default='Top 40')

    def id_setter(self, value):
        # Allocate IDs if DNE
        if value == '' or value is None or value == 'None':
            first, last = AdmissionsOfficer.allocate_ids(2)
            self.UpdateFromKey(ndb.Key('AdmissionsOfficer', first))
        elif not isinstance(value, basestring) and not isinstance(value, int):
            raise endpoints.BadRequestException('ID not string or int')
        else:
            self.UpdateFromKey(ndb.Key('AdmissionsOfficer', value))

    @EndpointsAliasProperty(setter=id_setter, required=True)
    def id(self):
        if self.key is not None:
            return str(self.key.id())


class Customer(User):
    """ Client Model """

    gpa = ndb.FloatProperty(required=True)
    tests = ndb.KeyProperty(repeated=True)
    essays = ndb.StringProperty(repeated=True)
    colleges = ndb.KeyProperty(repeated=True)
    helpMeWith = ndb.StringProperty(repeated=True)


class Test(EndpointsModel):
    """ Test Model """
    TEST_CHOICES = []

    type = ndb.StringProperty(required=True, choices=TEST_CHOICES)
    score = ndb.IntegerProperty(required=False)

