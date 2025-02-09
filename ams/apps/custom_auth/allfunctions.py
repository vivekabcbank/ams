import base64
from django.db import models

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
    ids = model.objects.all().values_list("id",flat=True)
    return [encode_str(id) for id in ids]

def get_dencoded_ids(ids):
    return [decode_str(id) for id in ids.split(",")]

def encoded_id(obj):
    # A common method to get the encoded ID of a model instance.
    return encode_str(obj.id)