__author__ = 'Brendan'

import sys
sys.path.insert(0, 'lib')

from endpoint_classes import *
from models import *
import endpoints


APPLICATION = endpoints.api_server([HyperAdmit], restricted=False)