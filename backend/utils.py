__author__ = 'brendan'
import endpoints
from protorpc import message_types
from protorpc import messages
from google.appengine.ext import ndb
DEBUG = True
USER_AUTH_RC = endpoints.ResourceContainer(message_types.VoidMessage,
                                           email=messages.StringField(1, required=True),
                                           password=messages.StringField(2, required=True))

USER_RC = endpoints.ResourceContainer(message_types.VoidMessage,
                                      user_id=messages.IntegerField(1, required=True),
                                      user_token=messages.StringField(2, required=True),
                                      last_cursor=messages.StringField(3, required=False),
                                      school_type=messages.StringField(4, required=False),
                                      college_rank=messages.StringField(5, required=False))

USER_NEW_RC = endpoints.ResourceContainer(message_types.VoidMessage,
                                          email=messages.StringField(1, required=True),
                                          first_name=messages.StringField(2, required=True),
                                          last_name=messages.StringField(3, required=True),
                                          phone=messages.StringField(4, required=True),
                                          school_type=messages.StringField(5, required=True))


def get_stripe_api_key():
    if DEBUG:
        return "sk_test_5sR4GHddXZ1EK8kQ98t5Heuw"
    else:
        return "sk_live_HYGtqSOL9p66j235jkMAofVY"


def get_mail_username():
    return "yury191"


def get_mail_pass():
    return "Grodno123"