__author__ = 'Brendan'

from endpoint_classes import *
from models import *
import endpoints


APPLICATION = endpoints.api_server([HyperAdmit], restricted=True)