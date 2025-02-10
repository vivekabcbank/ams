from rest_framework import serializers
from django.core.validators import RegexValidator
from .serializervalidators import *
from .allfunctions import *

first_name = serializers.CharField(
    required=True,
    validators=[
        RegexValidator(
            regex=Regex.ALPHABETICS.value,
            message=(
                'First name must be Alphabetics'
            ),
        ),
    ],
    min_length=3,
    max_length=50,
    error_messages={
        'blank': "First Name can't be blank"
    },
    label='First name',
    help_text="Provide Your First Name"
)
last_name = serializers.CharField(
    required=True,
    validators=[
        RegexValidator(
            regex=Regex.ALPHABETICS.value,
            message=(
                'Last name must be Alphabetics'
            ),
        ),
    ],
    min_length=3,
    max_length=50,
    error_messages={
        'blank': "Last Name can't be blank"
    },
    label='Last name',
    help_text="Provide Your Last Name"
)
email = serializers.CharField(
    required=True,
    validators=[
        RegexValidator(
            regex=Regex.EMAIL.value,
            message=("Please provide an valid email")
        ),
        user_validate_email_creation
    ],
    error_messages={"blank": "Email can't be blank"},
    help_text="Provide your email"
)
username = serializers.CharField(
    required=False,
    validators=[
        user_validate_username_creation
    ],
    min_length=3,
    max_length=15,
    help_text="Provide your username"
)
usertype_id = serializers.CharField(
    required=True,
    error_messages={
        "blank": "Country can't be blank"
    }
)
gender = serializers.ChoiceField(
    required=True,
    choices=(
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Others"),
    ),
    error_messages={
        "blank": "Sex can't be blank"
    }
)
dob = serializers.DateField(
    required=True,
    error_messages={"blank": "Date of birth Birth can't be balnk"}
)
callingcode = serializers.CharField(
    required=True,
    validators=[
        RegexValidator(
            regex=Regex.NUMBERS.value,
            message=("Callingcode contains only numeric values")
        )
    ],
    min_length=1,
    max_length=15,
    error_messages={
        "blank": "Calling code can't be blank"
    },
    help_text="Provide your calling code"
)
phone = serializers.CharField(
    required=True,
    validators=[
        RegexValidator(
            regex=Regex.NUMBERS.value,
            message="Cellphone contains only space and numeric values"
        ),
        user_validate_mobile_creation
    ],
    min_length=3,
    max_length=15,
    error_messages={
        "blank": "Cellphone can't be blank"
    },
    help_text="Provide your phone number"
)
address = serializers.CharField(
    required=True,
    allow_blank=True,
)
pincode = serializers.CharField(
    required=True,
    validators=[
        RegexValidator(
            regex=Regex.NUMBERS.value,
            message="Pincode contains only space and numeric values"
        ),
        user_validate_mobile_creation
    ],
    allow_blank=True,
    max_length=20,
)
country_id = serializers.CharField(
    required=True,
    error_messages={
        "blank": "Country can't be blank"
    }
)
state_id = serializers.CharField(
    required=True,
    error_messages={
        "blank": "State can't be blank"
    }
)
city_id = serializers.CharField(
    required=True,
    error_messages={"blank": "City can't be blank"}
)

company_name = serializers.CharField(
    required=True,
    allow_blank=False,
    error_messages={
        "blank": "company name can't be blank"
    },
    max_length=250
)

latitude = serializers.CharField(required=True)

longitude = serializers.CharField(required=True)

sitename = serializers.CharField(
    required=True,
    allow_blank=False,
    error_messages={
        "blank": "sitename can't be blank"
    },
    max_length=250
)