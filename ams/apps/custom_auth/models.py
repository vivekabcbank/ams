from django.db import models
from django.contrib.auth.models import AbstractUser
from django import utils
from pdb import set_trace
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.conf import settings
from rest_framework.authtoken.models import Token

class UserType(models.Model):
    typename = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    isdeleted = models.BooleanField(default=False)
    createddate = models.DateTimeField(default=utils.timezone.now, blank=True)
    updateddate = models.DateTimeField(null=True)

    class Meta:
        db_table = 'usertype'
        verbose_name = 'Usertype'
        verbose_name_plural = 'Usertypes'

    def __str__(self):
        return f"{self.typename}"


class Country(models.Model):
    countryname = models.CharField(max_length=200, default="")
    sortname = models.CharField(max_length=200, default="")
    countrycode = models.CharField(max_length=200, default="")
    isdeleted = models.BooleanField(default=False)
    createddate = models.DateTimeField(default=utils.timezone.now, blank=True)
    updateddate = models.DateTimeField(null=True)

    class Meta:
        db_table = 'country'
        verbose_name = 'Country'
        verbose_name_plural = 'Contries'

    def __str__(self):
        return f"{self.countryname}"


class State(models.Model):
    countryid = models.ForeignKey(
        Country,
        related_name="state",
        on_delete=models.CASCADE
    )
    statename = models.CharField(max_length=200)
    isdeleted = models.BooleanField(default=False)
    createddate = models.DateTimeField(default=utils.timezone.now, blank=True)
    updateddate = models.DateTimeField(null=True)

    class Meta:
        db_table = 'state'
        verbose_name = 'State'
        verbose_name_plural = 'States'

    def __str__(self):
        return f"{self.statename}"


class City(models.Model):
    stateid = models.ForeignKey(
        State,
        related_name="city",
        on_delete=models.CASCADE
    )
    cityname = models.CharField(max_length=200)
    isdeleted = models.BooleanField(default=False)
    createddate = models.DateTimeField(default=utils.timezone.now, blank=True)
    updateddate = models.DateTimeField(null=True)

    class Meta:
        db_table = 'city'
        verbose_name = 'City'
        verbose_name_plural = 'Cities'

    def __str__(self):
        return f"{self.cityname}"


class Site(models.Model):
    sitename = models.CharField(max_length=200)
    address = models.TextField(
        default='',
        blank=True,
        null=True
    )
    country = models.ForeignKey(
        Country,
        related_name="sitecountry",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    state = models.ForeignKey(
        State,
        related_name="sitestate",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    city = models.ForeignKey(
        City,
        related_name="sitecity",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    latitude = models.CharField(
        default='',
        max_length=20,
        blank=True,
        null=True
    )
    longitude = models.CharField(
        default='',
        max_length=20,
        blank=True,
        null=True
    )
    isdeleted = models.BooleanField(default=False)
    createddate = models.DateTimeField(default=utils.timezone.now, blank=True)
    updateddate = models.DateTimeField(null=True)

    class Meta:
        db_table = 'site'
        verbose_name = 'Site'
        verbose_name_plural = 'Sites'

    def __str__(self):
        return f"{self.sitename}"


class Users(AbstractUser):
    usertype = models.ForeignKey(
        UserType,
        related_name="users",
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    image = models.TextField(
        max_length=200,
        default='',
        blank=True,
        null=True
    )

    gender = models.CharField(
        max_length=1,
        choices=(
            ('M', 'Male'),
            ('F', 'Female'),
            ('O', 'Others')
        ),
        null=True,
        blank=True
    )
    dob = models.DateField(
        blank=True,
        null=True,
        auto_now_add=False
    )

    callingcode = models.CharField(
        max_length=10,
        default='',
        blank=True,
        null=True
    )

    phone = models.CharField(
        max_length=20,
        default='',
        blank=True,
        null=True
    )

    address = models.TextField(
        default='',
        blank=True,
        null=True
    )

    pincode = models.CharField(
        default='',
        max_length=20,
        blank=True,
        null=True
    )
    country = models.ForeignKey(
        Country,
        related_name="country",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    state = models.ForeignKey(
        State,
        related_name="state",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )
    city = models.ForeignKey(
        City,
        related_name="city",
        on_delete=models.CASCADE,
        blank=True,
        null=True
    )

    isdeleted = models.BooleanField(default=False)
    createddate = models.DateTimeField(default=utils.timezone.now, blank=True)
    updateddate = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    def get_name(self):
        get_first_name = self.first_name
        get_last_name = self.last_name
        name = ""
        if get_first_name:
            if name:
                name = str(name) + " " + get_first_name
            else:
                name = str(name) + get_first_name
        if get_last_name:
            if name:
                name = str(name) + " " + str(get_last_name)
            else:
                name = str(name) + str(get_last_name)
        return name

    def __str__(self):
        return f"{self.username}"


class Employee(models.Model):
    user = models.ForeignKey(
        Users,
        related_name="employeeinformation",
        on_delete=models.CASCADE,
        null=True
    )
    site_info = models.ForeignKey(
        Site,
        related_name="siteinformation",
        on_delete=models.CASCADE,
        null=True
    )
    joiningdate = models.DateTimeField(null=True)
    min_wages = models.FloatField(default=0.0)
    qualification = models.CharField(default='', max_length=250)
    isdeleted = models.BooleanField(default=False)
    createddate = models.DateTimeField(default=utils.timezone.now, blank=True)
    updateddate = models.DateTimeField(null=True)

    class Meta:
        db_table = 'employee'
        verbose_name = 'Employee'
        verbose_name_plural = 'employees'

    def __str__(self):
        return f"{self.user.username}"


class Attendance(models.Model):
    user = models.ForeignKey(
        Users,
        related_name="employeeattendance",
        on_delete=models.CASCADE,
        null=True
    )
    site_info = models.ForeignKey(
        Site,
        related_name="siteattendance",
        on_delete=models.CASCADE,
        null=True
    )

    attendance = models.CharField(
        max_length=1,
        choices=(
            ('P', 'Present'),
            ('A', 'Absent'),
            ('H', 'Half_day')
        ),
        null=True,
        blank=True
    )
    date = models.DateTimeField(null=True)
    isdeleted = models.BooleanField(default=False)
    createddate = models.DateTimeField(default=utils.timezone.now, blank=True)
    updateddate = models.DateTimeField(null=True)

    class Meta:
        db_table = 'attendance'
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendances'

    def __str__(self):
        return f"{self.user.username}"


class Leave(models.Model):
    user = models.ForeignKey(
        Users,
        related_name="employeealeave",
        on_delete=models.CASCADE,
        null=True
    )
    site_info = models.ForeignKey(
        Site,
        related_name="siteleave",
        on_delete=models.CASCADE,
        null=True
    )

    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    reason = models.TextField(blank=True, null=True)
    isdeleted = models.BooleanField(default=False)
    createddate = models.DateTimeField(default=utils.timezone.now, blank=True)
    updateddate = models.DateTimeField(null=True)

    class Meta:
        db_table = 'leave'
        verbose_name = 'Leave'
        verbose_name_plural = 'Leaves'

    def __str__(self):
        return f"{self.user.username}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
