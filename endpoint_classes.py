__author__ = 'Brendan'
import sys
sys.path.insert(0, 'libs')
from google.appengine.ext import ndb
import endpoints

from webapp2_extras.auth import InvalidPasswordError, InvalidAuthIdError
from protorpc import messages
from protorpc import message_types
from protorpc import remote
from models import AdmissionsOfficer
from models import User
from utils import *


@endpoints.api(name='hyperadmit', version='v1',
               allowed_client_ids=[endpoints.API_EXPLORER_CLIENT_ID],
               scopes=[endpoints.EMAIL_SCOPE])
class HyperAdmit(remote.Service):
    """ HyperAdmit API v1 """

    @endpoints.method(USER_AUTH_RC,
                      AdmissionsOfficer.ProtoModel(),
                      path='authuser', http_method='POST', name='auth_user')
    def auth_user(self, request):
        try:
            user = User.get_by_auth_password(request.email, request.password)
        except (InvalidPasswordError, InvalidAuthIdError):
            raise endpoints.ForbiddenException('NAW GET OUT')
        token, ts = User.create_auth_token(user.key.id())

    @endpoints.method(message_types.VoidMessage,
                      AdmissionsOfficer.ProtoCollection(),
                      path='getalladdOffs', http_method='POST', name='get_all_addOffs')
    def get_all_adOffs(self, request):
        query = AdmissionsOfficer.query()
        ad_offs = query.fetch()
        return AdmissionsOfficer.ToMessageCollection(ad_offs)

    # Ad Off methods
    @AdmissionsOfficer.method(request_fields=('id',),
                              path='getadoff/{id}', http_method='GET', name='get_ad_off')
    def get_ad_off(self, ad_off):

        if not ad_off.from_datastore:
            raise endpoints.NotFoundException('MyModel not found.')
        return ad_off

    @AdmissionsOfficer.method(request_fields=('email', 'last_name', 'first_name', 'phone'),
                              path='insertadoff', http_method='POST', name='insert_ad_off')
    def insert_ad_off(self, ad_off):
        if ad_off.from_datastore:
            raise endpoints.NotFoundException('BLAH')
        ad_off.school = 'UPenn'
        ad_off.school_type = 'Undergrad'
        ad_off.location = 'NYC'
        ad_off.hours_consulted = 0
        ad_off.knowledge_areas = ['Resume', 'Essays']
        ad_off.whoami = 'Im The BEST!'
        ad_off.howcanihelp = 'Being Awesome'
        ad_off.job_title = 'Admissions Director'
        ad_off.college_rank = 'Top 40'
        ad_off.alias = ad_off.email
        new_ad_off = AdmissionsOfficer(email=ad_off.email, first_name=ad_off.first_name, last_name=ad_off.last_name,
                                       phone=ad_off.phone,
                                       verified=ad_off.verified, school=ad_off.school, school_type=ad_off.school_type,
                                       location=ad_off.location, rating=ad_off.rating,
                                       hours_consulted=ad_off.hours_consulted,
                                       knowledge_areas=ad_off.knowledge_areas, whoami=ad_off.whoami,
                                       job_title=ad_off.job_title, howcanihelp=ad_off.howcanihelp,
                                       college_rank=ad_off.college_rank, alias=ad_off.alias)

        ret_ad_off_key = new_ad_off.put()
        ret_ad_off = ret_ad_off_key.get()
        return ret_ad_off

    @AdmissionsOfficer.query_method(user_required=False,
                                    query_fields=('school_type', 'college_rank', 'limit', 'order', 'pageToken'),
                                    path='getadoff', name='get_ad_off_list')
    def get_ad_off_list(self, query):

        return query
