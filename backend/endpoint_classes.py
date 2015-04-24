__author__ = 'Brendan'
import sys
sys.path.insert(0, 'lib')
sys.path.insert(0, 'stripe')
from webapp2_extras.auth import InvalidPasswordError, InvalidAuthIdError
from protorpc import remote
from backend.models import AdmissionsOfficer
from backend.models import User
from backend.models import FreeUser
from backend.utils import *
from sendgrid import SendGridClient
from sendgrid import Mail

import stripe

centralparkedu = endpoints.api(name='centralparkedu', version='v1',
                               allowed_client_ids=[endpoints.API_EXPLORER_CLIENT_ID],
                               scopes=[endpoints.EMAIL_SCOPE])


@centralparkedu.api_class(resource_name='hyperadmit', path='hyperadmit')
class HyperAdmit(remote.Service):
    """ HyperAdmit API v1 """

    @endpoints.method(USER_NEW_RC,
                      FreeUser.ProtoModel(),
                      path='freetrialsignup', http_method='POST', name='free_trial_signup')
    def free_trial_signup(self, request):

        new_user = FreeUser(email=request.email, first_name=request.first_name, last_name=request.last_name,
                            phone=request.phone, school_type=request.school_type)

        ret_user = new_user.put()

        return FreeUser.ToMessage(ret_user)

    @endpoints.method(path='sendemail', http_method='POST', name='send_email')
    def send_email(self, request):
        # make a secure connection to SendGrid
        sg = SendGridClient(get_mail_username(), get_mail_pass(), secure=True)

        # make a message object
        message = Mail()
        message.set_subject('message subject')
        message.set_html('<strong>HTML message body</strong>')
        message.set_text('plaintext message body')
        message.set_from('from@example.com')

        # add a recipient
        message.add_to('John Doe <yury191@gmail.com>')

        # use the Web API to send your message
        sg.send(message)
        return message_types.VoidMessage()

    @endpoints.method(USER_AUTH_RC,
                      AdmissionsOfficer.ProtoModel(),
                      path='authuser', http_method='POST', name='auth_user')
    def auth_user(self, request):
        try:
            user = User.get_by_auth_password(request.email, request.password)
        except (InvalidPasswordError, InvalidAuthIdError):
            raise endpoints.ForbiddenException('NAW GET OUT')
        token, ts = User.create_auth_token(user.key.id())

    @endpoints.method(USER_RC,
                      AdmissionsOfficer.ProtoCollection(),
                      path='getalladdOffs', http_method='POST', name='get_all_addOffs')
    def get_all_adOffs(self, request):
        user, ts = User.get_by_auth_token(int(request.user_id), request.user_token)
        if user is None:
            raise endpoints.ForbiddenException('User auth failed')

        cursor = None
        if request.last_cursor:
            cursor = ndb.Cursor.from_websafe_string(request.last_cursor)

        school_type = None
        if request.school_type and request.school_type != '':
            school_type = request.school_type

        college_rank = None
        if request.college_rank and request.college_rank != '':
            college_rank = request.college_rank

        if school_type and college_rank:
            ad_off_query = AdmissionsOfficer.query(AdmissionsOfficer.college_rank == college_rank,
                                                   AdmissionsOfficer.school_type == school_type).order(-AdmissionsOfficer.created,
                                                                                                       AdmissionsOfficer.key)
        elif school_type and not college_rank:
            ad_off_query = AdmissionsOfficer.query(AdmissionsOfficer.school_type == school_type).order(-AdmissionsOfficer.created,
                                                                                                       AdmissionsOfficer.key)
        elif not school_type and college_rank:
            ad_off_query = AdmissionsOfficer.query(AdmissionsOfficer.college_rank == college_rank).order(-AdmissionsOfficer.created,
                                                                                                         AdmissionsOfficer.key)
        else:
            ad_off_query = AdmissionsOfficer.query().order(-AdmissionsOfficer.created, AdmissionsOfficer.key)

        ad_offs, next_cursor, more = ad_off_query.fetch_page(10, start_cursor=cursor)

        ret_ad_off = AdmissionsOfficer.ToMessageCollection(ad_offs, next_cursor=next_cursor)
        return ret_ad_off

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
                                    path='getadoffs', name='get_ad_off_list')
    def get_ad_off_list(self, query):

        return query
