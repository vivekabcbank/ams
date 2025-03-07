from django.urls import path
from .views import *

urlpatterns = [
    path(
        'insert-user-type',
        InsertUserTypeView_v1.as_view(),
        name="insert-user-type"
    ),
    path(
        'get-usertypes',
        GetUserTypes_v1.as_view(),
        name="get-usertypes"
    ),
    path(
        'make-superviser',
        MakeSuperviserView_v1.as_view(),
        name="make-superviser"
    ),
    path(
        'insert-site',
        InsertSiteView_v1.as_view(),
        name="insert-site"
    ),path(
        'apply-leave',
        ApplyLeaveView_v1.as_view(),
        name="apply-leave"
    ),path(
        'get-sites',
        GetSitesView_v1.as_view(),
        name="get-sites"
    ),path(
        'get-employee',
        GetEmployeeView_v1.as_view(),
        name="get-employee"
    ),path(
        'mark-attendance',
        MarkAttendanceView_v1.as_view(),
        name="mark-attendance"
    ),

    # path(
    #     'insert-country',
    #     InsertCountryView_v1.as_view(),
    #     name="insert-country"
    # ),
    # path(
    #     'insert-state',
    #     InsertStateView_v1.as_view(),
    #     name="insert-state"
    # ),
    # path(
    #     'insert-city',
    #     InsertCityView_v1.as_view(),
    #     name="insert-city"
    # ),
    #
    # path(
    #     'get-state-by-country',
    #     GetStateByCountry_v1.as_view(),
    #     name="get-state-by-country"
    # ),
    # path(
    #     'get-city-by-state',
    #     GetCityByState_v1.as_view(),
    #     name="get-city-by-state"
    # ),
    # path(
    #     'get-country',
    #     GetCountry_v1.as_view(),
    #     name="get-country"
    # ),
]
