from pdb import set_trace

from .allfunctions import decode_str
from .models import Users, Site, UserType, Employee
from rest_framework import serializers


def user_validate_email_creation(value):
    if value != "" and value != None:
        result = Users.objects.filter(email__iexact=value, isdeleted=False).count()
        if result > 0:
            raise serializers.ValidationError("Provided email already in use")
    return value


def user_validate_mobile_creation(value):
    if value != "" and value != None:
        result = Users.objects.filter(phone__exact=value, isdeleted=False).count()
        if result > 0:
            raise serializers.ValidationError("Provided phone number already in use")
    return value


def user_validate_username_creation(value):
    if value != "" and value != None:
        result = Users.objects.filter(username__iexact=value, isdeleted=False).count()
        if result > 0:
            raise serializers.ValidationError("Provided username already in use")
    return value


def validate_user_identity(value=None):
    if value:
        try:
            if not Users.objects.filter(
                    id=int(decode_str(value)),
                    isdeleted=False,
            ).exists():
                raise serializers.ValidationError("User Identity doesn't valid.1")

        except ValueError:
            raise serializers.ValidationError("User Identity doesn't valid.2")

    return value


def validate_site_info_identity(value=None):
    if value:
        try:
            if not Site.objects.filter(
                    id=int(decode_str(value)),
                    isdeleted=False,
            ).exists():
                raise serializers.ValidationError("Site Identity doesn't valid.1")

        except ValueError:
            raise serializers.ValidationError("Site Identity doesn't valid.2")

    return value


def validate_usertype_identity(value=None):
    if value:
        try:
            if not UserType.objects.filter(
                    id=int(decode_str(value)),
                    isdeleted=False,
            ).exists():
                raise serializers.ValidationError("User type Identity doesn't valid.1")

        except ValueError:
            raise serializers.ValidationError("User type Identity doesn't valid.2")

    return value


def validate_employee_identity(value=None):
    if value:
        try:
            if not Employee.objects.filter(
                    id=int(decode_str(value)),
                    isdeleted=False,
            ).exists():
                raise serializers.ValidationError("Employee Identity doesn't valid.")

        except ValueError:
            raise serializers.ValidationError("Employee Identity doesn't valid.")

    return value
