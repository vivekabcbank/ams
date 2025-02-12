from django.urls import path
from .views import *

urlpatterns = [
    path(
        'insert-user-type',
        InsertUserTypeView.as_view(),
        name="insert-user-type"
    ),
    path(
        'get-usertypes',
        GetUserTypes.as_view(),
        name="get-usertypes"
    ),
    path(
        'make-superviser',
        MakeSuperviserView.as_view(),
        name="make-superviser"
    ),
    path(
        'insert-site',
        InsertSiteView.as_view(),
        name="insert-site"
    ),path(
        'apply-leave',
        ApplyLeaveView.as_view(),
        name="apply-leave"
    ),path(
        'get-sites',
        GetSitesView.as_view(),
        name="get-sites"
    ),path(
        'get-employee',
        GetEmployeeView.as_view(),
        name="get-employee"
    ),

    # path(
    #     'insert-country',
    #     InsertCountryView.as_view(),
    #     name="insert-country"
    # ),
    # path(
    #     'insert-state',
    #     InsertStateView.as_view(),
    #     name="insert-state"
    # ),
    # path(
    #     'insert-city',
    #     InsertCityView.as_view(),
    #     name="insert-city"
    # ),

    # path(
    #     'get-state-by-country',
    #     GetStateByCountry.as_view(),
    #     name="get-state-by-country"
    # ),
    # path(
    #     'get-city-by-state',
    #     GetCityByState.as_view(),
    #     name="get-city-by-state"
    # ),
    # path(
    #     'get-country',
    #     GetCountry.as_view(),
    #     name="get-country"
    # ),
]
