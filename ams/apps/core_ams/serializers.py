from rest_framework import serializers
from ..custom_auth.allfunctions import *
from ..custom_auth.models import *
from ..custom_auth.serializerfields import *


class ValidateSiteDetailsSerializers(serializers.Serializer):
    sitename = sitename
    address = address
    country_id = country_id
    state_id = state_id
    city_id = city_id
    latitude = latitude
    longitude = longitude

    @classmethod
    def validate(self, data):
        errors = {}
        sitename = data.get("sitename", "")
        country_id = data.get("country_id", 0)
        state_id = data.get("state_id", 0)
        city_id = data.get("city_id", 0)

        try:
            data["sitename"] = sitename
            if Site.objects.filter(sitename__exact=sitename,isdeleted=False).exists():
                errors['sitename'] = "Site name already exists"
        except Exception as e:
            errors['sitename'] = "Site name already exists"

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

        return super(ValidateSiteDetailsSerializers, self).validate(self, data)


class SiteDetailsSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    sitename = sitename
    address = address
    country_id = serializers.SerializerMethodField()
    state_id = serializers.SerializerMethodField()
    city_id = serializers.SerializerMethodField()
    latitude = latitude
    longitude = longitude

    class Meta:
        model = Site
        fields = ("id", 'sitename', 'address', 'country_id', 'state_id', 'city_id', 'latitude', 'longitude')

    def get_id(self, obj):
        return encode_str(obj.id)

    def get_country_id(self, obj):
        return encode_str(obj.country_id)

    def get_state_id(self, obj):
        return encode_str(obj.state_id)

    def get_city_id(self, obj):
        return encode_str(obj.city_id)


class CreateSiteSerializer(serializers.ModelSerializer):
    sitename = sitename
    address = address
    country_id = country_id
    state_id = state_id
    city_id = city_id
    latitude = latitude
    longitude = longitude

    class Meta:
        model = Site
        fields = (
            'sitename', 'address', 'country_id', 'state_id', 'city_id', 'latitude', 'longitude')


class MakeSuperviserSerializer(serializers.Serializer):
    user_id = serializers.CharField(required=True, help_text="Provide City Id")
    usertype_id = serializers.CharField(required=True, help_text="Provide State Id")

    @classmethod
    def validate(self, data):
        errors = {}
        usertype_id = data.get("usertype_id", 0)
        user_id = data.get("user_id", 0)

        try:
            user_id = int(decode_str(user_id))
            data["user_id"] = user_id
            user = Users.objects.filter(pk=user_id,
                                        isdeleted=False)
            data["user"] = user
            if not user.exists():
                errors['user_id'] = "Invalid user id"
        except Exception as e:
            errors['user_id'] = "Invalid user id"

        try:
            usertype_id = int(decode_str(usertype_id))
            data["usertype_id"] = usertype_id
            if not UserType.objects.filter(id=usertype_id,
                                           isdeleted=False).exists():
                errors['usertype_id'] = "Invalid usertype id"
        except Exception as e:
            errors['usertype_id'] = "Invalid usertype id"

        if errors:
            raise serializers.ValidationError(errors)

        return super(MakeSuperviserSerializer, self).validate(self, data)


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


class UserTypeSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()

    class Meta:
        model = UserType
        fields = ("id", "typename", 'description')

    def get_id(self, obj):
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
