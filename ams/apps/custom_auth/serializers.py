from .models import *
from .serializerfields import *
from django.db.models.functions import Concat
from django.db.models import Q


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
                if not Users.objects.filter(
                        Q(usertype_id=User_Type_id.ADMIN.value) |
                        Q(is_superuser=True),
                        Q(id=userauth),
                        Q(isdeleted=False)
                ).exists():
                    errors["userauth"] = "Admin Identity doesn't valid."
            except Exception as e:
                errors["userauth"] = "Admin Identity doesn't valid."
        else:
            errors["userauth"] = "Admin Identity doesn't valid."

        if errors:
            raise serializers.ValidationError(errors)
        return super(CheckAdminUserIdentitySerializer, self).validate(self, data)

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True,
                                     max_length=250,
                                     error_messages={'blank': "Email or phone number can't be blank"})
    password = serializers.CharField(required=True,
                                     max_length=250,
                                     error_messages={'blank': "Password can't be blank"})

    @classmethod
    def validate(self, data):
        errors = {}
        username = data.get('username')
        if not Users.objects.annotate(
            mobile=Concat('callingcode', 'phone')
        ).filter(
            Q(username__exact=username) |
            Q(email__iexact=username) |
            Q(mobile__exact=username),
            Q(isdeleted=False),
        ).exists():
            errors['username'] = "This account doesn't exist"

        if errors:
            raise serializers.ValidationError(errors)
        return super(UserLoginSerializer, self).validate(self, data)

class ValidateUserDetailsSerializers(serializers.Serializer):
    company_name = company_name
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

        return super(ValidateUserDetailsSerializers, self).validate(self, data)

class UserDetailsSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    company_name = company_name
    first_name = first_name
    last_name = last_name
    email = email
    username = username

    gender = gender
    dob = dob
    callingcode = callingcode
    phone = phone
    address = address
    pincode = pincode
    country_id = serializers.SerializerMethodField()
    state_id = serializers.SerializerMethodField()
    city_id = serializers.SerializerMethodField()
    usertype_id = serializers.SerializerMethodField()

    class Meta:
        model = Users
        fields = ("id",'first_name', 'last_name', 'email', 'username', 'usertype_id', 'gender', 'dob', 'callingcode', 'phone',
            'address', 'pincode', 'country_id', 'state_id', 'city_id',"company_name")

    def get_id(self, obj):
        return encode_str(obj.id)

    def get_country_id(self, obj):
        return encode_str(obj.country_id)

    def get_usertype_id(self, obj):
        return encode_str(obj.usertype_id)

    def get_state_id(self, obj):
        return encode_str(obj.state_id)

    def get_city_id(self, obj):
        return encode_str(obj.city_id)

class CreateUserSerializer(serializers.ModelSerializer):
    company_name = company_name
    first_name = first_name
    last_name = last_name
    email = email
    username = username
    gender = gender
    dob = dob
    callingcode = callingcode
    phone = phone
    address = address
    pincode = pincode

    usertype_id = usertype_id
    country_id = country_id
    state_id = state_id
    city_id = city_id

    class Meta:
        model = Users
        fields = (
            'first_name', 'last_name', 'email', 'username', 'gender', 'dob', 'callingcode', 'phone',
            'address', 'pincode',"usertype_id", "country_id", "state_id","city_id","company_name")

    @classmethod
    def validate(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')

        data['username'] = set_username(first_name,last_name)

        return data