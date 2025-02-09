
from .models import Users
from rest_framework import serializers
def user_validate_email_creation(value):
    if value != "" and value != None:
        result = Users.objects.filter(email__iexact = value, isdeleted=False).count()
        if result > 0:
            raise serializers.ValidationError("Provided email already in use")
    return  value

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