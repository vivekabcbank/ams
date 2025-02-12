from django.contrib.auth.backends import ModelBackend
from django.contrib.gis.measure import pretty_name

from .models import Users
from .allfunctions import check_password
from django.db.models import Q
from django.db.models.functions import Concat
from pdb import set_trace

class UserAuthentication(ModelBackend):
    @staticmethod
    def user_authenticate(request=None, **credentials):

        global user_pwd, username
        if "username" in credentials:
            username = credentials["username"]

        if "password" in credentials:
            user_pwd = credentials["password"]

        try:
            user = Users.objects.annotate(
                mobile=Concat('callingcode', 'phone')
            ).filter(
                Q(username__exact=username) |
                Q(mobile__exact=username),
                Q(isdeleted=False),
            ).last()
            success = check_password(user.password, user_pwd)
            if success:
                return user
        except Exception as e:
            print(f"Exception:  {e}")
        return None


class MiddlewarePrintRequest:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            print(f"Request method: {request.method}")
            print(f"Request path: {request.path}")

            print("Request headers:")
            for header, value in request.headers.items():
                print(f"{header}: {value}")

            if request.method == "POST":
                print("Request body:")
                print(request.body.decode('utf-8'))

            response = self.get_response(request)

            response['X-Custom-Header'] = 'This is a custom header'
        except Exception as e:
            print(e)
        response = self.get_response(request)
        return response
