__author__ = 'Brendan'

from lib.endpoints_proto_datastore import ndb
from endpoint_classes import *
from models import *
import endpoints


APPLICATION = endpoints.api_server([HyperAdmit], restricted=False)