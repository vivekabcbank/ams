# Cmd + Alt + L
# apply validations for all, like int should not take alphabate, like apply regex validation
# exact: Case-sensitive exact match.
# iexact: Case-insensitive exact match.
# before commit check can we optimize code again, check all property access specifiers like @static, cls, self, @classmethod and many more
# NGRock
# https://9385-114-143-222-190.ngrok-free.app/swagger/
# remove default usertype_id = data.get("usertype_id", 0) => 0 from all places and test
"""
        try:
            owner_user_id = int(decode_str(owner_user_id))
            data["owner_user_id"] = owner_user_id
            if not Users.objects.filter(pk=owner_user_id,isdeleted=False).exists():
                errors['owner_user_id'] = "Invalid owner id"
        except Exception as e:
            errors['owner_user_id'] = "Invalid owner id"

add common logic like for each table can set, check medirec project
"""
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
    path(
        'insert-employee',
        InsertEmployeeView.as_view(),
        name="insert-employee"
    ),

]
