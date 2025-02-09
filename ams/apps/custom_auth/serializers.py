from .models import *
from .serializerfields import *

class CheckAdminUserIdentitySerializer(serializers.Serializer):
    userauth = serializers.CharField(required=True, allow_blank=False,
                                     error_messages={'blank': 'Userauth can\'t be blank'})

    @classmethod
    def validate(self, data):
        errors = {}
        userauth = data.get("userauth", "")
        if is_not_Empty(userauth):
            try:
                userauth = int(decode_str(userauth))
                data["userauth"] = userauth
                if not Users.objects.filter(id=userauth,
                                            isdeleted=False,
                                            usertype_id=User_Type_id.ADMIN.value,
                                            ).exists():
                    errors["userauth"] = "Admin Identity doesn't valid."
            except Exception as e:
                errors["userauth"] = "Admin Identity doesn't valid."
        else:
            errors["userauth"] = "Admin Identity doesn't valid."

        if errors:
            raise serializers.ValidationError(errors)
        return super(CheckAdminUserIdentitySerializer, self).validate(self, data)


class InsertUserTypeSerializer(serializers.ModelSerializer):
    typename = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "blank": "Type name can't be blank"
        }
    )

    description = serializers.CharField(
        required=False,
        allow_blank=True
    )

    class Meta:
        model = UserType
        fields = ('typename', 'description')

    @classmethod
    def validate(self, data):
        errors = {}
        typename = data.get("typename", "")

        if is_not_Empty(typename):
            if UserType.objects.filter(typename=typename).exists():
                errors["typename"] = "Type name already exists"
        else:
            errors["typename"] = "Type name is required"

        if errors:
            raise serializers.ValidationError(errors)
        return super(InsertUserTypeSerializer, self).validate(self, data)


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
    countryid = serializers.CharField(
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
        fields = ('countryid', 'statename')

    @classmethod
    def validate(self, data):
        errors = {}
        countryid = data.get("countryid", "")

        try:
            countryid = int(decode_str(countryid))
            data["countryid"] = countryid
            if not Country.objects.filter(id=countryid,
                                          isdeleted=False
                                          ).exists():
                errors["countryid"] = "Country Identity doesn't valid."
        except Exception as e:
            errors["countryid"] = "Country Identity doesn't valid."
        if errors:
            raise serializers.ValidationError(errors)

        return super(InsertStateSerializer, self).validate(self, data)


class InsertCitySerializer(serializers.ModelSerializer):
    stateid = serializers.CharField(
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
        fields = ('stateid', 'cityname')

    @classmethod
    def validate(self, data):
        errors = {}
        stateid = data.get("stateid", "")

        try:
            stateid = int(decode_str(stateid))
            data["stateid"] = stateid
            if not State.objects.filter(id=stateid,
                                        isdeleted=False
                                        ).exists():
                errors["stateid"] = "State Identity doesn't valid."
        except Exception as e:
            errors["stateid"] = "State Identity doesn't valid."
        if errors:
            raise serializers.ValidationError(errors)

        return super(InsertCitySerializer, self).validate(self, data)


class CountrySerializer(serializers.ModelSerializer):
    encoded_id = serializers.SerializerMethodField()

    class Meta:
        model = Country
        fields = ("id", "encoded_id", "countryname", "sortname", 'countrycode')

    def get_encoded_id(self, obj):
        return encode_str(obj.id)


class StateSerializer(serializers.ModelSerializer):
    encoded_id = serializers.SerializerMethodField()
    encoded_country_id = serializers.SerializerMethodField()

    class Meta:
        model = State
        fields = ("id", "encoded_id", "encoded_country_id", "statename", 'countryid')

    def get_encoded_id(self, obj):
        return encode_str(obj.id)

    def get_encoded_country_id(self, obj):
        return encode_str(obj.countryid_id)


class CitySerializer(serializers.ModelSerializer):
    encoded_id = serializers.SerializerMethodField()
    encoded_stateid_id = serializers.SerializerMethodField()

    class Meta:
        model = City
        fields = ("id", "encoded_id", "encoded_stateid_id", "cityname", 'stateid_id')

    def get_encoded_id(self, obj):
        return encode_str(obj.id)

    def get_encoded_stateid_id(self, obj):
        return encode_str(obj.stateid_id)


class UserTypeSerializer(serializers.ModelSerializer):
    encoded_id = serializers.SerializerMethodField()

    class Meta:
        model = UserType
        fields = ("id", "encoded_id", "typename", 'description')

    def get_encoded_id(self, obj):
        return encode_str(obj.id)


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


class UserDetailsSerializers(serializers.Serializer):
    first_name = first_name
    last_name = last_name
    email = email
    username = username
    usertype_id = usertype_id
    gender = gender
    dob = dob
    callingcode = callingcode
    phone = phone
    address = address
    pincode = pincode
    country_id = country_id
    state_id = state_id
    city_id = city_id

    password = serializers.CharField(required=True,
                                     allow_blank=False,
                                     min_length=6,
                                     max_length=30,
                                     error_messages={'blank': "Password can't be blank"},
                                     help_text="Provide Your Password")
    @classmethod
    def validate(self, data):
        errors = {}
        usertype_id = data.get("usertype_id", 0)
        country_id = data.get("country_id", 0)
        state_id = data.get("state_id", 0)
        city_id = data.get("city_id", 0)

        try:
            usertype_id = int(decode_str(usertype_id))
            data["usertype_id"] = usertype_id
            if not UserType.objects.filter(id=usertype_id,
                                           isdeleted=False).exists():
                errors['usertype_id'] = "Invalid usertype id"
        except Exception as e:
            errors['usertype_id'] = "Invalid usertype id"

        try:
            country_id = int(decode_str(country_id))
            data["country_id"] = country_id
            if not Country.objects.filter(id=country_id,
                                          isdeleted=False).exists():
                errors['country_id'] = "Invalid country id"
        except Exception as e:
            errors['country_id'] = "Invalid country id"

        try:
            state_id = int(decode_str(state_id))
            data["state_id"] = state_id
            if not State.objects.filter(id=state_id,
                                        isdeleted=False).exists():
                errors['state_id'] = "Invalid state id"
        except Exception as e:
            errors['state_id'] = "Invalid state id"

        try:
            city_id = int(decode_str(city_id))
            data["city_id"] = city_id
            if not City.objects.filter(id=city_id,
                                       isdeleted=False).exists():
                errors['city_id'] = "Invalid city id"
        except Exception as e:
            errors['city_id'] = "Invalid city id"

        if errors:
            raise serializers.ValidationError(errors)

        return super(UserDetailsSerializers, self).validate(self, data)


class CreateUserSerializer(serializers.ModelSerializer):
    first_name = first_name
    last_name = last_name
    email = email
    username = username
    usertype_id = usertype_id
    gender = gender
    dob = dob
    callingcode = callingcode
    phone = phone
    address = address
    pincode = pincode
    country_id = country_id
    state_id = state_id
    city_id = city_id

    encoded_usertype_id = serializers.SerializerMethodField()
    encoded_country_id = serializers.SerializerMethodField()
    encoded_state_id = serializers.SerializerMethodField()
    encoded_city_id = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = (
        'first_name', 'last_name', 'email', 'username', 'usertype_id', 'gender', 'dob', 'callingcode', 'phone',
        'address', 'pincode', 'country_id', 'state_id', 'city_id', "encoded_usertype_id", "encoded_country_id",
        "encoded_state_id", "encoded_city_id")

    def get_encoded_usertype_id(self, obj):
        return encode_str(obj.usertype_id)

    def get_encoded_country_id(self, obj):
        return encode_str(obj.country_id)

    def get_encoded_state_id(self, obj):
        return encode_str(obj.state_id)

    def get_encoded_city_id(self, obj):
        return encode_str(obj.city_id)

    @classmethod
    def validate(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        data['username'] = set_username(first_name, last_name)

        return data
