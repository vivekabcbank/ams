from django.contrib import admin
from .models import *
from .allfunctions import *

admin_class_name = get_admin_class_name(Country)
class admin_class_name(admin.ModelAdmin):
    list_display = (encoded_id, "id",  "isdeleted")
admin.site.register(Country, admin_class_name)

admin_class_name = get_admin_class_name(State)
class admin_class_name(admin.ModelAdmin):
    list_display = (encoded_id, "id",  "isdeleted")
admin.site.register(State, admin_class_name)

admin_class_name = get_admin_class_name(City)
class admin_class_name(admin.ModelAdmin):
    list_display = (encoded_id, "id",  "isdeleted")
admin.site.register(City, admin_class_name)

class UsersAdmin(admin.ModelAdmin):
    list_display = ("id","user_name","usertype","gender")
admin.site.register(Users, UsersAdmin)

admin_class_name = get_admin_class_name(UserType)
class admin_class_name(admin.ModelAdmin):
    list_display = (encoded_id, "id",  "isdeleted")
admin.site.register(UserType, admin_class_name)

admin_class_name = get_admin_class_name(Site)
class admin_class_name(admin.ModelAdmin):
    list_display = (encoded_id, "id",  "isdeleted")
admin.site.register(Site, admin_class_name)

admin_class_name = get_admin_class_name(Employee)
class admin_class_name(admin.ModelAdmin):
    list_display = (encoded_id, "id",  "isdeleted")
admin.site.register(Employee, admin_class_name)

admin_class_name = get_admin_class_name(Attendance)
class admin_class_name(admin.ModelAdmin):
    list_display = (encoded_id, "id",  "isdeleted")
admin.site.register(Attendance, admin_class_name)

admin_class_name = get_admin_class_name(Leave)
class admin_class_name(admin.ModelAdmin):
    list_display = (encoded_id, "id",  "isdeleted")
admin.site.register(Leave, admin_class_name)