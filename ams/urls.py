"""
URL configuration for ams project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from .views import *
from django.conf.urls import handler404

schema_view = get_schema_view(
   openapi.Info(
      title="My API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@myapi.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('',Index,name="index"),
    path('api/v1/admin/', admin.site.urls),
    path('api/v1/auth/',include('ams.apps.custom_auth.urls')),
    path('api/v1/core/',include('ams.apps.core_ams.urls')),
    path('api/v1/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='swagger-schema'),
]

handler404 = custom_404

# Writing test cases in all apps Django, flask, fast-api, also do any one implementations like payment getways
# Optimize all apps Django, flask, fast-api with needed requirements
# implement logger, caching in all thrree apps
