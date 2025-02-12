from logging import setLoggerClass

from rest_framework.generics import GenericAPIView
from .serializers import *
from rest_framework.response import Response
from .http_status_code import *
from .authsetup import UserAuthentication
from django.contrib.auth import login, logout
from pdb import set_trace


class InsertEmployeeView(GenericAPIView):

    @classmethod
    def post(cls, request):
        response = {}

        other_data = ValidateEmployeeDetailsSerializers(data=request.data)
        is_other_data_valid = other_data.is_valid()

        if is_other_data_valid:
            posted_data = other_data.validated_data
            user_serializer = CreateUserSerializer(data=posted_data)
            user_serializer_is_valid = user_serializer.is_valid()

            if user_serializer_is_valid:
                user = user_serializer.save()
                # user_details_serializer = UserDetailsSerializer(user)
                employee = cls.create_emp(user, posted_data)
                response = {
                    "employee_id": encode_str(employee.id),
                    "message": "Employee added successfully",
                    'status': HTTP_200_OK
                }
            else:
                response['errors'] = get_json_errors(user_serializer.errors)
                response['status'] = HTTP_204_NO_CONTENT
        else:
            response['errors'] = get_json_errors(
                other_data.errors
            )
            response['status'] = HTTP_204_NO_CONTENT

        return Response(response)

    @classmethod
    def create_emp(cls, user, posted_data):
        employee = Employee.objects.create(
            user=user,
            site_info_id=posted_data.get("site_info_id"),
            joiningdate=posted_data.get("joiningdate"),
            min_wages=posted_data.get("min_wages"),
            qualification=posted_data.get("qualification")
        )
        return employee

class UserSignUpView(GenericAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = ValidateUserDetailsSerializers

    @classmethod
    def post(cls, request):
        response = {}

        other_data = ValidateUserDetailsSerializers(data=request.data)
        is_other_data_valid = other_data.is_valid()

        if is_other_data_valid:
            posted_data = other_data.validated_data
            password = posted_data.get("password")
            user_serializer = CreateUserSerializer(data=posted_data)

            user_serializer_is_valid = user_serializer.is_valid()
            if user_serializer_is_valid:
                user = user_serializer.save()
                user.password = hash_md5(password)
                user.save()

                user_details_serializer = UserDetailsSerializer(user)
                response = {
                    "result": user_details_serializer.data,
                    "message": "User created successfully",
                    'status': HTTP_200_OK
                }
            else:
                response['errors'] = get_json_errors(user_serializer.errors)
                response['status'] = HTTP_204_NO_CONTENT
        else:
            response['errors'] = get_json_errors(
                other_data.errors
            )
            response['status'] = HTTP_204_NO_CONTENT

        return Response(response)


class UserSigninView(GenericAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = UserLoginSerializer

    @classmethod
    def post(self, request):
        response = {}
        other_data = UserLoginSerializer(data=request.data)

        if other_data.is_valid():
            posted_data = other_data.validated_data
            username = posted_data.get('username')
            password = posted_data.get('password')

            user = UserAuthentication.user_authenticate(username=username, password=password)
            if user:
                response = {
                    "result": UserDetailsSerializer(user).data,
                    "token": get_authentication_token(user.id),
                    "message": "Logged in successfully",
                    'status': HTTP_200_OK
                }
                login(request, user)

            else:
                response['errors'] = {"error": 'Wrong username or password'}
                response['status'] = 201
        else:
            response['errors'] = get_json_errors(other_data.errors)
            response['status'] = 201
        return Response(response)
