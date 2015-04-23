import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), "lib"))
sys.path.append(os.path.join(os.path.dirname(__file__), "stripe"))
from backend.endpoint_classes import *
import endpoints


APPLICATION = endpoints.api_server([HyperAdmit], restricted=False)