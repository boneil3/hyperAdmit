__author__ = 'Brendan'
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
from endpoints_proto_datastore.ndb.model import EndpointsModel
from endpoints_proto_datastore.ndb.properties import EndpointsAliasProperty
from google.appengine.ext import ndb
import endpoints
import webapp2_extras.appengine.auth.models


class User(EndpointsModel, webapp2_extras.appengine.auth.models.User):
    """ User Base Model """

    email = ndb.StringProperty(required=True)
    first_name = ndb.StringProperty(required=True)
    last_name = ndb.StringProperty(required=True)
    phone = ndb.StringProperty(required=True)
    stripeCustId = ndb.StringProperty(default=None)
    stripeCardId = ndb.StringProperty(default=None)
    stripeChargeId = ndb.StringProperty(default=None, repeated=True)
    alias = ndb.StringProperty(default=None)
    appointments = ndb.KeyProperty(repeated=True)

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
            return self.key.id()


class AdmissionsOfficer(User):
    """ Admissions Officer Model """

    _message_fields_schema = ('id', 'verified', 'school', 'school_type', 'location', 'rating', 'hours_consulted',
                              'last_active', 'knowledge_areas', 'whoami', 'job_title', 'howcanihelp', 'college_rank')
    verified = ndb.BooleanProperty(default=False)
    paymentStuff = ndb.StringProperty(default=None)
    school = ndb.KeyProperty(repeated=True)
    school_type = ndb.StringProperty(default=None)
    location = ndb.StringProperty(default=None)
    rating = ndb.FloatProperty(default=0.0)
    hours_consulted = ndb.IntegerProperty(default=0)
    last_active = ndb.DateTimeProperty()
    knowledge_areas = ndb.StringProperty(repeated=True)
    whoami = ndb.StringProperty(default='')
    howcanihelp = ndb.StringProperty(default='')
    job_title = ndb.StringProperty(default='')
    college_rank = ndb.IntegerProperty(default=0)


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


class University(EndpointsModel):
    """ University Institution Model """
    UNIV_TYPES = []

    rank = ndb.IntegerProperty(required=True)
    name = ndb.StringProperty(required=True)
    type = ndb.StringProperty(required=True, choices=UNIV_TYPES)
    major = ndb.StringProperty(required=False)
