from django.contrib import admin
from .models import *
from .allfunctions import *

admin_class_name = get_admin_class_name(Country)
class admin_class_name(admin.ModelAdmin):
    list_display = (encoded_id, "id","countryname","sortname", "countrycode", "isdeleted")
admin.site.register(Country, admin_class_name)

admin_class_name = get_admin_class_name(State)
class admin_class_name(admin.ModelAdmin):
    list_display = (encoded_id, "id", "statename", "isdeleted")
admin.site.register(State, admin_class_name)

admin_class_name = get_admin_class_name(City)
class admin_class_name(admin.ModelAdmin):
    list_display = (encoded_id, "id", "cityname", "isdeleted")
admin.site.register(City, admin_class_name)

admin_class_name = get_admin_class_name(Users)
class admin_class_name(admin.ModelAdmin):
    list_display = (encoded_id, "id","username","usertype")
admin.site.register(Users, admin_class_name)

admin_class_name = get_admin_class_name(UserType)
class admin_class_name(admin.ModelAdmin):
    list_display = (encoded_id, "id", "typename", "isdeleted")
admin.site.register(UserType, admin_class_name)

admin_class_name = get_admin_class_name(Site)
class admin_class_name(admin.ModelAdmin):
    list_display = (encoded_id, "id", "owner_user","sitename","address","city", "isdeleted")
admin.site.register(Site, admin_class_name)

admin_class_name = get_admin_class_name(Employee)
class admin_class_name(admin.ModelAdmin):
    list_display = (encoded_id, "id", "user","site_info","joiningdate","min_wages","qualification","isdeleted")
admin.site.register(Employee, admin_class_name)

admin_class_name = get_admin_class_name(Attendance)
class admin_class_name(admin.ModelAdmin):
    list_display = (encoded_id, "id", "employee", "site_info","attendance","date" ,"isdeleted")
admin.site.register(Attendance, admin_class_name)

admin_class_name = get_admin_class_name(Leave)
class admin_class_name(admin.ModelAdmin):
    list_display = (encoded_id, "id","employee","site_info", "start_date", "end_date","reason","isdeleted")
admin.site.register(Leave, admin_class_name)