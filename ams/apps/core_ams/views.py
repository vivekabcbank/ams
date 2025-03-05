from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from ..custom_auth.serializers import *
from .serializers import *
from ..custom_auth.http_status_code import *
from rest_framework.response import Response

class MarkAttendanceView(GenericAPIView):
    serializer_class = MarkAttendanceSerializer
    @classmethod
    def post(cls, request):
        response = {}

        other_data = MarkAttendanceSerializer(data=request.data)
        is_other_data_valid = other_data.is_valid()

        if is_other_data_valid:
            posted_data = other_data.validated_data
            json_list = posted_data.get("json_list")

            [Attendance.objects.create(
                employee_id=item["employee_id"],
                site_info_id=item["site_info_id"],
                attendance=item["attendance"],
                date=item["date"],
            ) for item in json_list]

            response['message'] = "Attendance added successfully"
            response['status'] = HTTP_200_OK
        else:
            response['errors'] = get_json_errors(
                other_data.errors
            )
            response['status'] = HTTP_204_NO_CONTENT

        return Response(response)

class GetEmployeeView(GenericAPIView):

    serializer_class = GetEmployeeSerializer

    @classmethod
    def get(cls, request):
        response = {}
        request_data = {}
        request_data["site_info_id"] = request.GET.get("site_info_id")
        other_data = GetEmployeeSerializer(data=request_data)
        is_other_data_valid = other_data.is_valid()

        if is_other_data_valid:
            posted_data = other_data.validated_data
            site_info_id = posted_data.get("site_info_id")
            result = Employee.objects.filter(site_info_id=site_info_id)
            employee_serializer = EmployeeDetailsSerializer(result, many=True)
            response['result'] = employee_serializer.data
            response['status'] = HTTP_200_OK
        else:
            response['errors'] = get_json_errors(
                other_data.errors
            )
            response['status'] = HTTP_204_NO_CONTENT

        return Response(response)


class GetSitesView(GenericAPIView):
    serializer_class = GetSitesSerializer

    @classmethod
    def get(cls, request):
        response = {}
        request_data = {}
        request_data["usertype_id"] = request.GET.get("usertype_id")
        request_data["owner_user_id"] = request.GET.get("owner_user_id")
        other_data = GetSitesSerializer(data=request_data)
        is_other_data_valid = other_data.is_valid()

        if is_other_data_valid:
            posted_data = other_data.validated_data
            admin_sites = posted_data.get("admin_sites")
            employee_sites = posted_data.get("employee_sites")
            if admin_sites:
                result_serializer = SiteDetailsSerializer(admin_sites, many=True)
            else:
                result_serializer = SiteDetailsSerializer(employee_sites,)
            response['sites'] = result_serializer.data
            response['status'] = HTTP_200_OK
        else:
            response['errors'] = get_json_errors(
                other_data.errors
            )
            response['status'] = HTTP_204_NO_CONTENT

        return Response(response)

class ApplyLeaveView(GenericAPIView):
    serializer_class = ApplyLeaveSerializers

    @classmethod
    def post(cls, request):
        response = {}

        other_data = ApplyLeaveSerializers(data=request.data)
        is_other_data_valid = other_data.is_valid()

        if is_other_data_valid:
            posted_data = other_data.validated_data
            leave_serializer = CreateLeaveSerializer(data=posted_data)
            leave_serializer_is_valid = leave_serializer.is_valid()

            if leave_serializer_is_valid:
                leave_serializer.create(validated_data=posted_data)
                response = {
                    "message": "Leave added successfully",
                    'status': HTTP_200_OK
                }
            else:
                response['errors'] = get_json_errors(leave_serializer.errors)
                response['status'] = HTTP_204_NO_CONTENT
        else:
            response['errors'] = get_json_errors(
                other_data.errors
            )
            response['status'] = HTTP_204_NO_CONTENT

        return Response(response)

class InsertSiteView(GenericAPIView):
    serializer_class = ValidateSiteDetailsSerializers

    @classmethod
    def post(cls, request):
        response = {}

        other_data = ValidateSiteDetailsSerializers(data=request.data)
        is_other_data_valid = other_data.is_valid()

        if is_other_data_valid:
            posted_data = other_data.validated_data
            site_serializer = CreateSiteSerializer(data=posted_data)
            site_serializer_is_valid = site_serializer.is_valid()

            if site_serializer_is_valid:
                site = site_serializer.save()
                site_details_serializer = SiteDetailsSerializer(site)
                response = {
                    "result": site_details_serializer.data,
                    "message": "Site created successfully",
                    'status': HTTP_200_OK
                }
            else:
                response['errors'] = get_json_errors(site_serializer.errors)
                response['status'] = HTTP_204_NO_CONTENT
        else:
            response['errors'] = get_json_errors(
                other_data.errors
            )
            response['status'] = HTTP_204_NO_CONTENT

        return Response(response)

class MakeSuperviserView(GenericAPIView):
    serializer_class = MakeSuperviserSerializer

    @classmethod
    def post(cls, request):
        response = {}
        other_data = MakeSuperviserSerializer(data=request.data)
        is_other_data_valid = other_data.is_valid()

        if is_other_data_valid:
            posted_data = other_data.validated_data
            user = posted_data.get("user")
            password = posted_data.get("password")

            user.password = hash_md5(password)
            user.usertype_id = User_Type_id.SUPERVISER.value
            user.save()

            response['status'] = HTTP_200_OK
            response["message"] = "User changed to superuser"
        else:
            response['errors'] = get_json_errors(
                other_data.errors
            )
            response['status'] = HTTP_204_NO_CONTENT

        return Response(response)

class InsertUserTypeView(GenericAPIView):
    serializer_class = InsertUserTypeSerializer

    @classmethod
    def post(cls, request):
        response = {}

        authorization = CheckAdminUserIdentitySerializer(data=request.data)
        other_data = InsertUserTypeSerializer(data=request.data)

        is_authorization_valid = authorization.is_valid()
        is_other_data_valid = other_data.is_valid()

        if is_authorization_valid and is_other_data_valid:
            posted_data = other_data.validated_data
            user_type_serializer = InsertUserTypeSerializer(data=posted_data)
            if user_type_serializer.is_valid():
                user_type = user_type_serializer.save()
                response['status'] = HTTP_200_OK
                response["result"] = {"id": encode_str(user_type.id)}
                response["message"] = "User type added successfully"
            else:
                response['errors'] = get_json_errors(
                    user_type_serializer.errors,
                )
                response['status'] = HTTP_204_NO_CONTENT
        else:
            response['errors'] = collect_allErrors(
                authorization.errors,
                other_data.errors
            )
            response['status'] = HTTP_204_NO_CONTENT

        return Response(response)


class InsertCountryView(GenericAPIView):

    @classmethod
    def post(cls, request):
        response = {}

        authorization = CheckAdminUserIdentitySerializer(data=request.data)
        is_authorization_valid = authorization.is_valid()

        other_data = InsertCountrySerializer(data=request.data)
        is_other_data_valid = other_data.is_valid()

        if is_authorization_valid and is_other_data_valid:
            other_data.save()
            response['status'] = HTTP_200_OK
            response["message"] = "Country created successfully"
        else:
            response['errors'] = collect_allErrors(
                other_data.errors,
                authorization.errors
            )
            response['status'] = HTTP_204_NO_CONTENT

        return Response(response)


class InsertStateView(GenericAPIView):

    @classmethod
    def post(cls, request):
        response = {}
        authorization = CheckAdminUserIdentitySerializer(data=request.data)
        is_authorization_valid = authorization.is_valid()

        other_data = InsertStateSerializer(data=request.data)
        is_other_data_valid = other_data.is_valid()

        if is_authorization_valid and is_other_data_valid:
            other_data.save()
            response['status'] = HTTP_200_OK
            response["message"] = "State created successfully"
        else:
            response['errors'] = collect_allErrors(
                other_data.errors,
                authorization.errors
            )
            response['status'] = HTTP_204_NO_CONTENT

        return Response(response)


class InsertCityView(GenericAPIView):

    @classmethod
    def post(cls, request):

        response = {}
        authorization = CheckAdminUserIdentitySerializer(data=request.data)
        is_authorization_valid = authorization.is_valid()

        other_data = InsertCitySerializer(data=request.data)
        is_other_data_valid = other_data.is_valid()

        if is_authorization_valid and is_other_data_valid:
            other_data.save()
            response['status'] = HTTP_200_OK
            response["message"] = "City created successfully"
        else:
            response['errors'] = collect_allErrors(
                other_data.errors,
                authorization.errors
            )
            response['status'] = HTTP_204_NO_CONTENT

        return Response(response)


class GetStateByCountry(GenericAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = GetStateByCountrySerializer

    @classmethod
    def get(self, request):
        response = {}
        other_data = GetStateByCountrySerializer(data=request.data)

        if other_data.is_valid():
            posted_data = other_data.validated_data
            country_id = posted_data.get('country_id')
            state_id = posted_data.get('state_id')

            if state_id and country_id:
                result = State.objects.filter(pk=state_id,
                                              countryid_id=country_id,
                                              isdeleted=False).last()
                if result:
                    result_serializer = StateSerializer(result)
                    response['states'] = result_serializer.data
                    response['status'] = HTTP_200_OK
                else:
                    response['states'] = {}
                    response['status'] = 201
            elif state_id and country_id is None:
                result = State.objects.filter(pk=state_id,
                                              isdeleted=False).last()
                if result:
                    result_serializer = StateSerializer(result)
                    response['states'] = result_serializer.data
                    response['status'] = HTTP_200_OK
                else:
                    response['states'] = {}
                    response['status'] = 201
            elif state_id is None and country_id:
                result = State.objects.filter(countryid_id=country_id,
                                              isdeleted=False)
                if result:
                    result_serializer = StateSerializer(result, many=True)
                    response['states'] = result_serializer.data
                    response['status'] = HTTP_200_OK
                else:
                    response['states'] = {}
                    response['status'] = 201
            else:
                result = State.objects.filter(isdeleted=False)
                if result:
                    result_serializer = StateSerializer(result, many=True)
                    response['states'] = result_serializer.data
                    response['status'] = HTTP_200_OK
                else:
                    response['states'] = {}
                    response['status'] = 201
        else:
            response['errors'] = other_data.errors
            response['status'] = 201

        return Response(response)


class GetCityByState(GenericAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = GetCityByStateSerializer

    @classmethod
    def get(self, request):
        response = {}
        other_data = GetCityByStateSerializer(data=request.data)

        if other_data.is_valid():
            posted_data = other_data.validated_data
            city_id = posted_data.get('city_id')
            state_id = posted_data.get('state_id')

            if state_id and city_id:
                result = City.objects.filter(pk=city_id,
                                             stateid_id=state_id,
                                             isdeleted=False).last()
                if result:
                    result_serializer = CitySerializer(result)
                    response['cities'] = result_serializer.data
                    response['status'] = HTTP_200_OK
                else:
                    response['cities'] = {}
                    response['status'] = 201
            elif state_id and city_id is None:
                result = City.objects.filter(stateid_id=state_id,
                                             isdeleted=False).last()
                if result:
                    result_serializer = CitySerializer(result)
                    response['cities'] = result_serializer.data
                    response['status'] = HTTP_200_OK
                else:
                    response['cities'] = {}
                    response['status'] = 201
            elif state_id is None and city_id:
                result = City.objects.filter(pk=city_id,
                                             isdeleted=False)
                if result:
                    result_serializer = CitySerializer(result, many=True)
                    response['cities'] = result_serializer.data
                    response['status'] = HTTP_200_OK
                else:
                    response['cities'] = {}
                    response['status'] = 201
            else:
                result = City.objects.filter(isdeleted=False)
                if result:
                    result_serializer = CitySerializer(result, many=True)
                    response['cities'] = result_serializer.data
                    response['status'] = HTTP_200_OK
                else:
                    response['cities'] = {}
                    response['status'] = 201
        else:
            response['errors'] = other_data.errors
            response['status'] = 201

        return Response(response)


class GetCountry(GenericAPIView):
    authentication_classes = ()
    permission_classes = ()

    serializer_class = GetCountrySerializer

    @classmethod
    def get(self, request):
        response = {}
        other_data = GetCountrySerializer(data=request.data)

        if other_data.is_valid():
            posted_data = other_data.validated_data
            country_id = posted_data.get('country_id')

            if country_id:
                result = Country.objects.filter(pk=country_id,
                                                isdeleted=False)
                if result:
                    result_serializer = CountrySerializer(result, many=True)
                    response['countries'] = result_serializer.data
                    response['status'] = HTTP_200_OK
                else:
                    response['countries'] = {}
                    response['status'] = 201
            else:
                result = Country.objects.filter(isdeleted=False)
                if result:
                    result_serializer = CountrySerializer(result, many=True)
                    response['countries'] = result_serializer.data
                    response['status'] = HTTP_200_OK
                else:
                    response['countries'] = {}
                    response['status'] = 201
        else:
            response['errors'] = other_data.errors
            response['status'] = 201

        return Response(response)


class GetUserTypes(GenericAPIView):
    serializer_class = UserTypeSerializer

    @classmethod
    def get(self, request):
        response = {}

        result = UserType.objects.filter(isdeleted=False)
        if result:
            result_serializer = UserTypeSerializer(result, many=True)
            response['user_types'] = result_serializer.data
            response['status'] = HTTP_200_OK
        else:
            response['countries'] = {}
            response['status'] = 201

        return Response(response)
