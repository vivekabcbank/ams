from rest_framework import serializers
from django.core.validators import RegexValidator
from .serializervalidators import *
from .allfunctions import *
from .serializervalidators import *

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
    required=False,
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
    validators=[
        validate_usertype_identity
    ],
    error_messages={
        "blank": "Country can't be blank"
    }
)

usertype_id_without_vald = serializers.CharField(
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
    required=False,
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
    allow_blank=True,
)
country = serializers.CharField(
    required=True,
    error_messages={
        "blank": "Country can't be blank"
    }
)
state = serializers.CharField(
    required=True,
    error_messages={
        "blank": "State can't be blank"
    }
)
city = serializers.CharField(
    required=True,
    error_messages={"blank": "City can't be blank"}
)

site_info_id = serializers.CharField(
    required=True,
    validators=[
        validate_site_info_identity
    ],
    error_messages={"blank": "Site id can't be blank"}
)

qualification = serializers.CharField(
    required=True,
    error_messages={"blank": "qualification can't be blank"}
)

joiningdate = serializers.DateField(
    required=True,
    error_messages={"blank": "Joining date can't be balnk"}
)

min_wages = serializers.FloatField(
    required=True,
    error_messages={"blank": "min wages can't be balnk"}
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

owner_user_id = serializers.CharField(
    required=True,
    error_messages={"blank": "Owner id can't be balnk"}
)

is_on_leave = serializers.BooleanField(
    default=False
)

userauth = serializers.CharField(required=True,
                                 allow_blank=False,
                                 validators=[
                                     validate_user_identity
                                 ],
                                 error_messages={'blank': 'Userauth can\'t be blank'})

employee_id = serializers.CharField(required=True,
                                 allow_blank=False,
                                 validators=[
                                     validate_employee_identity
                                 ],
                                 error_messages={'blank': 'Userauth can\'t be blank'})

password = serializers.CharField(required=True,
                                     allow_blank=False,
                                     min_length=6,
                                     max_length=30,
                                     error_messages={'blank': "Password can't be blank"},
                                     help_text="Provide Your Password")

username_without_vald = serializers.CharField(required=True,
                                 max_length=250,
                                 error_messages={'blank': "Email or phone number can't be blank"})

description = serializers.CharField(
    required=False,
    allow_blank=True
)

typename = serializers.CharField(
        required=True,
        allow_blank=False,
        error_messages={
            "blank": "Type name can't be blank"
        }
    )

start_date = serializers.DateField(
    required=True,
    error_messages={"blank": "Start date can't be balnk"}
)
end_date = serializers.DateField(
    required=True,
    error_messages={"blank": "End date can't be balnk"}
)

site_info_id_without_vald = serializers.CharField(
    required=True,
    error_messages={"blank": "Site id can't be blank"}
)

employee_id_without_vald = serializers.CharField(required=True,
                                 allow_blank=False,
                                 error_messages={'blank': 'Userauth can\'t be blank'})

reason = serializers.CharField(required=True, help_text="provide reason")