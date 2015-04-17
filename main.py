__author__ = 'Brendan'

import sys
sys.path.append('lib')

from endpoint_classes import *
from models import *
import endpoints


APPLICATION = endpoints.api_server([HyperAdmit], restricted=True)