__author__ = 'brendan'
import endpoints
from protorpc import message_types
from protorpc import messages
from google.appengine.ext import ndb

USER_AUTH_RC = endpoints.ResourceContainer(message_types.VoidMessage,
                                           email=messages.StringField(1, required=True),
                                           password=messages.StringField(2, required=True))

USER_RC = endpoints.ResourceContainer(message_types.VoidMessage,
                                      user_id=messages.IntegerField(1, required=True),
                                      user_token=messages.StringField(2, required=True),
                                      last_cursor=messages.StringField(3, required=False))