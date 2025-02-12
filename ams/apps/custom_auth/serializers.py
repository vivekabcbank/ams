from .models import *
from .serializerfields import *
from django.db.models.functions import Concat
from django.db.models import Q
from .serializervalidators import *

class CheckAdminUserIdentitySerializer(serializers.Serializer):
    userauth = userauth

    @classmethod
    def validate(cls, data):
        errors = {}
        data["userauth"] = userauth = decode_id(data.get("userauth"))
        try:
            if not Users.objects.filter(
                    Q(usertype_id=User_Type_id.ADMIN.value) |
                    Q(is_superuser=True),
                    Q(id=userauth),
                    Q(isdeleted=False)
            ).exists():
                errors["userauth"] = "Admin Identity doesn't valid."
        except Exception as e:
            errors["userauth"] = "Admin Identity doesn't valid."

        if errors:
            raise serializers.ValidationError(errors)
        return super(CheckAdminUserIdentitySerializer, cls).validate(cls, data)


class UserLoginSerializer(serializers.Serializer):
    username = username_without_vald
    password = password

    @classmethod
    def validate(cls, data):
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
        return super(UserLoginSerializer, cls).validate(cls, data)


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
    country = country
    state = state
    city = city
    password = password

    @classmethod
    def validate(self, data):
        data["usertype_id"] = decode_id(data.get("usertype_id"))
        return data


class UserDetailsSerializer(serializers.ModelSerializer):
    id = serializers.SerializerMethodField()
    first_name = first_name
    last_name = last_name
    username = username
    gender = gender
    callingcode = callingcode
    phone = phone
    address = address
    pincode = pincode
    country = country
    state = state
    city = city
    company_name = company_name
    usertype_id = serializers.SerializerMethodField()
    dob = dob
    email = email

    class Meta:
        model = Users
        fields = (
            "id", 'first_name', 'last_name', 'email', 'username', 'usertype_id', 'gender', 'dob', 'callingcode',
            'phone', 'address', 'pincode', 'country', 'state', 'city', "company_name")

    def get_id(self, obj):
        return encode_str(obj.id)

    def get_usertype_id(self, obj):
        return encode_str(obj.usertype_id)


class CreateUserSerializer(serializers.ModelSerializer):
    first_name = first_name
    last_name = last_name
    username = username
    gender = gender
    callingcode = callingcode
    phone = phone
    address = address
    pincode = pincode
    usertype_id = usertype_id_without_vald
    country = country
    state = state
    city = city
    company_name = company_name
    email = email
    dob = dob

    class Meta:
        model = Users
        fields = (
            'first_name', 'last_name', 'email', 'username', 'gender', 'dob', 'callingcode', 'phone',
            'address', 'pincode', "usertype_id", "country", "state", "city", "company_name")

    @classmethod
    def validate(self, data):
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        data['username'] = set_username(first_name, last_name)
        return data


class ValidateEmployeeDetailsSerializers(serializers.Serializer):
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
    country = country
    state = state
    city = city
    usertype_id = usertype_id
    site_info_id = site_info_id
    joiningdate = joiningdate
    min_wages = min_wages
    qualification = qualification

    @classmethod
    def validate(self, data):
        data["usertype_id"] = decode_id(data.get("usertype_id"))
        data["site_info_id"] = decode_id(data.get("site_info_id"))
        return data
