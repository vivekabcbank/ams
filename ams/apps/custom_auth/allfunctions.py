import base64
from django.db import models
from enum import Enum
from jsonmerge import merge
import uuid
import hashlib
from .models import Users
from rest_framework.authtoken.models import Token
import datetime


def decode_str(encrypt_text):
    decode = base64.b64decode(encrypt_text).decode('ascii')
    return decode


def encode_str(text):
    string = str(text)
    encode = base64.b64encode(string.encode('ascii'))
    return str(encode.decode('ascii'))


def get_admin_class_name(cls_name: models.Model):
    return f"{cls_name.__name__}Admin"


def get_encoded_ids(model: models.Model):
    ids = model.objects.all().values_list("id", flat=True)
    return [encode_str(id) for id in ids]


def get_dencoded_ids(ids):
    return [decode_str(id) for id in ids.split(",")]


def encoded_id(obj):
    # A common method to get the encoded ID of a model instance.
    return encode_str(obj.id)


def is_Empty(string: str):
    if string == "" or string == '':
        return True
    return False


def is_not_Empty(string: str):
    if string != "" and string != '':
        return True
    return False


class User_Type_id(Enum):
    ADMIN = 1
    SUPERVISER = 2
    EMPLOYEE = 3


class Regex(Enum):
    ALPHABETICS = r'^[a-zA-Z]*$'
    EMAIL = r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$'
    NUMBERS = r'^[0-9]*$'
    ALPHANUMERIC = r'^[a-zA-Z0-9 -]*$'


class Date_Formats(Enum):
    YY_MM_DD_H_M_S = "%Y-%m-%d %H:%M:%S"
    Month_Date_Year = "%b %d, %Y"


def collect_allErrors(errors1=None, errors2=None):
    errors1 = get_json_errors(errors1)
    errors2 = get_json_errors(errors2)

    errors = merge(errors1, errors2)

    return errors


def get_json_errors(error_list_data):
    __field_errors = {}

    field_errors = [(k, v[0]) for k, v in error_list_data.items()]

    for key, error_list in field_errors:
        __field_errors[key] = error_list

    return __field_errors


def hash_md5(token):
    salt = uuid.uuid4().hex
    return hashlib.sha256(
        salt.encode() + token.encode()
    ).hexdigest() + ':' + salt


def get_username(token=None):
    return token


def get_authentication_token(userid):
    user = Users.objects.get(pk=userid)
    token, created = Token.objects.get_or_create(user=user)
    token_key = created.key if created else token.key
    return token_key


def set_username(first_name=None, last_name=None, check=0):
    name = ""
    now_timestamp = datetime.datetime.now().timestamp()
    if first_name != None or first_name != "":
        name = first_name

    if last_name != None or last_name != "":
        name = f"{name}.{last_name}"
    name = name + str(now_timestamp)

    return name


def valid_url_extension(url, extension_list):
    # http://stackoverflow.com/a/10543969/396300
    return any([url.endswith(e) for e in extension_list])


def replace_all(text, dic):
    for i, j in dic.items():
        text = text.replace(i, j)
    return text


def get_weekdays(day=None):
    days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
    if day:
        i = days.index(day)  # get the index of the selected day
        d1 = days[i:]  # get the list from an including this index
        d1.extend(days[:i])  # append the list form the beginning to this index
    else:
        d1 = days
    return d1


def check_password(hashed_password, user_password):
    try:
        password, salt = hashed_password.split(':')
        return password == hashlib.sha256(
            salt.encode() + user_password.encode()
        ).hexdigest()
    except Exception as e:
        print(e)
        return False


def decode_id(id):
    return int(decode_str(id))


def decode_multi_value(value):
    if value:
        value = value.split(",")
        try:
            value = [int(decode_str(x)) for x in value]
        except ValueError:
            value = []
    else:
        value = []
    return value
