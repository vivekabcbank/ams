from ..custom_auth.models import *
from ..custom_auth.serializerfields import *


class GetEmployeeSerializer(serializers.Serializer):
    site_info_id = site_info_id

    @classmethod
    def validate(self, data):
        data["site_info_id"] = decode_id(data.get("site_info_id"))
        return data


class ApplyLeaveSerializers(serializers.Serializer):
    employee_id = employee_id
    site_info_id = site_info_id
    start_date = start_date
    end_date = end_date
    reason = reason

    @classmethod
    def validate(self, data):
        errors = {}
        data["employee_id"] = employee_id = decode_id(data.get("employee_id"))
        data["site_info_id"] = site_info_id = decode_id(data.get("site_info_id"))
        start_date = data.get("start_date")
        end_date = data.get("end_date")

        if start_date >= end_date:
            errors['date mismatch'] = "End date shoule be grater than start date"

        try:
            if employee_id is not None and site_info_id is not None:
                if not Employee.objects.filter(id=employee_id,
                                               site_info_id=site_info_id,
                                               isdeleted=False).exists():
                    errors['mismatch_data'] = "employee_id, site not matched"
        except Exception as e:
            errors['mismatch_data'] = "employee_id, site not matchedee"

        if errors:
            raise serializers.ValidationError(errors)

        return super(ApplyLeaveSerializers, self).validate(self, data)


class CreateLeaveSerializer(serializers.ModelSerializer):
    employee_id = employee_id_without_vald
    site_info_id = site_info_id_without_vald
    start_date = start_date
    end_date = end_date
    reason = reason

    class Meta:
        model = Leave
        fields = ('employee_id', 'site_info_id', 'start_date', 'end_date', 'reason')


class ValidateSiteDetailsSerializers(serializers.Serializer):
    owner_user_id = userauth
    sitename = sitename
    address = address
    country = country
    state = state
    city = city
    latitude = latitude
    longitude = longitude

    @classmethod
    def validate(self, data):
        errors = {}
        sitename = data.get("sitename")
        data["owner_user_id"] = owner_user_id = decode_id(data.get("owner_user_id"))

        try:
            if Site.objects.filter(sitename__exact=sitename,
                                   owner_user_id=owner_user_id,
                                   isdeleted=False).exists():
                errors['sitename'] = "Site name already exists"
        except Exception as e:
            errors['sitename'] = "Site name already exists"

        if errors:
            raise serializers.ValidationError(errors)

        return super(ValidateSiteDetailsSerializers, self).validate(self, data)


class SiteDetailsSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    sitename = sitename
    address = address
    country = country
    state = state
    city = city
    latitude = latitude
    longitude = longitude
    owner_user_id = serializers.SerializerMethodField()

    class Meta:
        model = Site
        fields = ("id", 'sitename', 'address', 'country', 'state', 'city', 'latitude', 'longitude', "owner_user_id")

    def get_id(self, obj):
        return encode_str(obj.id)

    def get_owner_user_id(self, obj):
        return encode_str(obj.owner_user_id)


class GetSitesSerializer(serializers.Serializer):
    owner_user_id = owner_user_id
    usertype_id = usertype_id

    @classmethod
    def validate(self, data):
        errors = {}
        data["usertype_id"] = usertype_id = decode_id(data.get("usertype_id", ""))

        try:
            data["owner_user_id"] = owner_user_id = decode_id(data.get("owner_user_id"))
            if usertype_id == User_Type_id.ADMIN.value:
                user = Users.objects.filter(pk=owner_user_id, isdeleted=False).first()
                data["admin_sites"] = Site.objects.filter(owner_user_id=owner_user_id,
                                                          isdeleted=False)
            else:
                user = Employee.objects.filter(pk=owner_user_id).select_related('site_info').first()
                data["employee_sites"] = user.site_info
            if not user:
                errors['owner_user_id'] = "Invalid user id"

        except Exception as e:
            errors['owner_user_id'] = "Invalid owner id"

        if errors:
            raise serializers.ValidationError(errors)

        return super(GetSitesSerializer, self).validate(self, data)


class CreateSiteSerializer(serializers.ModelSerializer):
    sitename = sitename
    address = address
    country = country
    state = state
    city = city
    latitude = latitude
    longitude = longitude
    owner_user_id = owner_user_id

    class Meta:
        model = Site
        fields = (
            'sitename', 'address', 'country', 'state', 'city', 'latitude', 'longitude', "owner_user_id")


class MakeSuperviserSerializer(serializers.Serializer):
    employee_id = employee_id
    usertype_id = usertype_id
    password = password

    @classmethod
    def validate(self, data):
        errors = {}
        data["usertype_id"] = decode_id(data.get("usertype_id"))
        data["employee_id"] = employee_id = decode_id(data.get("employee_id"))

        try:
            employee = Employee.objects.filter(pk=employee_id,
                                               isdeleted=False).first()

            user = Users.objects.filter(pk=employee.user.id,
                                        isdeleted=False).first()
            data["user"] = user
        except Exception as e:
            errors['user_id'] = "Invalid employee id"

        if errors:
            raise serializers.ValidationError(errors)

        return super(MakeSuperviserSerializer, self).validate(self, data)


class UserTypeSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = UserType
        fields = ("id", "typename", 'description')

    def get_id(self, obj):
        return encode_str(obj.id)


class InsertUserTypeSerializer(serializers.ModelSerializer):
    typename = typename
    description = description

    class Meta:
        model = UserType
        fields = ('typename', 'description')

    @classmethod
    def validate(self, data):
        errors = {}
        typename = data.get("typename")
        if UserType.objects.filter(typename=typename).exists():
            errors["typename"] = "Type name already exists"
        if errors:
            raise serializers.ValidationError(errors)
        return super(InsertUserTypeSerializer, self).validate(self, data)


class EmployeeDetailsSerializer(serializers.ModelSerializer):
    joiningdate = joiningdate
    min_wages = min_wages
    qualification = qualification
    is_on_leave = serializers.SerializerMethodField()
    id = serializers.SerializerMethodField()
    user_id = serializers.SerializerMethodField()
    site_info_id = serializers.SerializerMethodField()

    class Meta:
        model = Employee
        fields = (
            "id", 'user_id', 'site_info_id', 'joiningdate', 'min_wages', 'qualification', "is_on_leave")

    def get_id(self, obj):
        return encode_str(obj.id)

    def get_user_id(self, obj):
        return encode_str(obj.user_id)

    def get_site_info_id(self, obj):
        return encode_str(obj.site_info_id)

    def get_is_on_leave(self, obj):
        leave = Leave.objects.filter(employee_id=obj.id).first()
        if leave and leave.start_date and leave.end_date:
            today = datetime.date.today()
            if today == leave.start_date or leave.start_date < today < leave.end_date:
                return True
        return False


class InsertCountrySerializer(serializers.ModelSerializer):
    countryname = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "blank": "Type name can't be blank"
        }
    )

    sortname = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "blank": "Type name can't be blank"
        }
    )

    countrycode = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "blank": "Type name can't be blank"
        }
    )

    class Meta:
        model = Country
        fields = ('countryname', 'sortname', "countrycode")

    @classmethod
    def validate(self, data):
        errors = {}
        countryname = data.get("countryname", "")
        sortname = data.get("sortname", "")
        countrycode = data.get("countrycode", "")

        if Country.objects.filter(countryname=countryname,
                                  sortname=sortname,
                                  countrycode=countrycode).exists():
            errors["typename"] = "Country name already exists"

        if errors:
            raise serializers.ValidationError(errors)

        return super(InsertCountrySerializer, self).validate(self, data)


class InsertStateSerializer(serializers.ModelSerializer):
    countryid_id = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "blank": "Type name can't be blank"
        }
    )

    statename = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "blank": "Type name can't be blank"
        }
    )

    class Meta:
        model = State
        fields = ('countryid_id', 'statename')

    @classmethod
    def validate(self, data):
        errors = {}
        countryid_id = data.get("countryid_id", "")
        statename = data.get("statename", "")

        try:
            countryid_id = int(decode_str(countryid_id))
            data["countryid_id"] = countryid_id
            if not Country.objects.filter(id=countryid_id,
                                          isdeleted=False
                                          ).exists():
                errors["countryid_id"] = "Country Identity doesn't valid."
        except Exception as e:
            errors["countryid_id"] = "Country Identity doesn't valid."

        try:
            if State.objects.filter(statename=statename,
                                    isdeleted=False
                                    ).exists():
                errors["statename"] = "State name already exists"
        except Exception as e:
            errors["statename"] = "State name already exists"

        if errors:
            raise serializers.ValidationError(errors)

        return super(InsertStateSerializer, self).validate(self, data)


class InsertCitySerializer(serializers.ModelSerializer):
    stateid_id = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "blank": "Type name can't be blank"
        }
    )

    cityname = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "blank": "Type name can't be blank"
        }
    )

    class Meta:
        model = City
        fields = ('stateid_id', 'cityname')

    @classmethod
    def validate(self, data):
        errors = {}
        stateid_id = data.get("stateid_id", "")
        cityname = data.get("cityname", "")

        try:
            stateid_id = int(decode_str(stateid_id))
            data["stateid_id"] = stateid_id
            if not State.objects.filter(id=stateid_id,
                                        isdeleted=False
                                        ).exists():
                errors["stateid_id"] = "State Identity doesn't valid."
        except Exception as e:
            errors["stateid_id"] = "State Identity doesn't valid."

        try:
            if City.objects.filter(cityname=cityname,
                                   isdeleted=False
                                   ).exists():
                errors["cityname"] = "City name already exists"
        except Exception as e:
            errors["cityname"] = "City name already exists"

        if errors:
            raise serializers.ValidationError(errors)

        return super(InsertCitySerializer, self).validate(self, data)


class CountrySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ("id", "countryname", "sortname", 'countrycode')

    def get_id(self, obj):
        return encode_str(obj.id)


class StateSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    country_id = serializers.SerializerMethodField()

    class Meta:
        model = State
        fields = ("id", "country_id", "statename", 'countryid')

    def get_id(self, obj):
        return encode_str(obj.id)

    def get_country_id(self, obj):
        return encode_str(obj.countryid_id)


class CitySerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    stateid_id = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ("id", "stateid_id", "cityname", 'stateid_id')

    def get_id(self, obj):
        return encode_str(obj.id)

    def get_stateid_id(self, obj):
        return encode_str(obj.stateid_id)


class GetCityByStateSerializer(serializers.Serializer):
    city_id = serializers.CharField(required=False, help_text="Provide City Id")
    state_id = serializers.CharField(required=False, help_text="Provide State Id")

    @classmethod
    def validate(self, data):
        errors = {}
        city_id = data.get("city_id")
        state_id = data.get("state_id")

        if city_id:
            try:
                city_id = int(decode_str(city_id))
                data["city_id"] = city_id
                city = City.objects.filter(id=city_id,
                                           isdeleted=False)
                if not city.exists():
                    errors['city_id'] = "Invalid city id"
            except Exception as e:
                errors['city_id'] = "Invalid city id"

        if state_id:
            try:
                state_id = int(decode_str(state_id))
                data["state_id"] = state_id
                state = State.objects.filter(id=state_id,
                                             isdeleted=False)
                if not state.exists():
                    errors['state_id'] = "Invalid state id"
            except Exception as e:
                errors['state_id'] = "Invalid state id"

        if errors:
            raise serializers.ValidationError(errors)

        return super(GetCityByStateSerializer, self).validate(self, data)


class GetStateByCountrySerializer(serializers.Serializer):
    country_id = serializers.CharField(required=False, help_text="Provide Country Id")
    state_id = serializers.CharField(required=False, help_text="Provide State Id")

    @classmethod
    def validate(self, data):
        errors = {}
        country_id = data.get("country_id")
        state_id = data.get("state_id")

        if country_id:
            try:
                country_id = int(decode_str(country_id))
                data["country_id"] = country_id
                country = Country.objects.filter(id=country_id,
                                                 isdeleted=False)
                if not country.exists():
                    errors['country_id'] = "Invalid country id"
            except Exception as e:
                errors['country_id'] = "Invalid country id"

        if state_id:
            try:
                state_id = int(decode_str(state_id))
                data["state_id"] = state_id
                state = State.objects.filter(id=state_id,
                                             isdeleted=False)
                if not state.exists():
                    errors['state_id'] = "Invalid state id"
            except Exception as e:
                errors['state_id'] = "Invalid state id"

        if errors:
            raise serializers.ValidationError(errors)

        return super(GetStateByCountrySerializer, self).validate(self, data)


class GetCountrySerializer(serializers.Serializer):
    country_id = serializers.CharField(required=False, help_text="Provide Country Id")

    @classmethod
    def validate(self, data):
        errors = {}
        country_id = data.get("country_id")

        if country_id:
            try:
                country_id = int(decode_str(country_id))
                data["country_id"] = country_id
                country = Country.objects.filter(id=country_id,
                                                 isdeleted=False)
                if not country.exists():
                    errors['country_id'] = "Invalid country id"
            except Exception as e:
                errors['country_id'] = "Invalid country id"

        if errors:
            raise serializers.ValidationError(errors)

        return super(GetCountrySerializer, self).validate(self, data)
