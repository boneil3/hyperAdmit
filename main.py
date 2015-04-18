import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
from endpoint_classes import *
import endpoints


APPLICATION = endpoints.api_server([HyperAdmit], restricted=False)