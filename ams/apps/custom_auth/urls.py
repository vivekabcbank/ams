# Cmd + Alt + L
# apply validations for all, like int should not take alphabate, like apply regex validation
# exact: Case-sensitive exact match.
# iexact: Case-insensitive exact match.
# before commit check can we optimize code again, check all property access specifiers like @static, cls, self, @classmethod and many more
# NGRock
from django.urls import path
from .views import *

urlpatterns = [
    path(
        'signup-user',
        UserSignUpView.as_view(),
        name="signup-user"
    ),
    path(
        'signin-user',
        UserSigninView.as_view(),
        name="signin-user"
    ),
]
