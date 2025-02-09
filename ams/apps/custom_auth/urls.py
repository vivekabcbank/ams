# Cmd + Alt + L
# apply validations for all, like int should not take alphabate, like apply regex validation
from django.urls import path
from .views import *

urlpatterns = [
    path(
        'insert-user-type',
        InsertUserTypeView.as_view(),
        name="insert-user-type"
    ),

    path(
        'create-user',
        CreateUserView.as_view(),
        name="create-user"
    ),
    path(
        'insert-country',
        InsertCountryView.as_view(),
        name="insert-country"
    ),
    path(
        'insert-state',
        InsertStateView.as_view(),
        name="insert-state"
    ),
    path(
        'insert-city',
        InsertCityView.as_view(),
        name="insert-city"
    ),

    path(
        'get-state-by-country',
        GetStateByCountry.as_view(),
        name="get-state-by-country"
    ),
    path(
        'get-city-by-state',
        GetCityByState.as_view(),
        name="get-city-by-state"
    ),
    path(
        'get-country',
        GetCountry.as_view(),
        name="get-country"
    ),
    path(
        'get-usertypes',
        GetUserTypes.as_view(),
        name="get-usertypes"
    ),
]
