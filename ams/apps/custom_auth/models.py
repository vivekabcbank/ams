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
        verbose_name_plural = 'Usertype'

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
        verbose_name_plural = 'Country'

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
        verbose_name_plural = 'State'

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
        verbose_name_plural = 'City'

    def __str__(self):
        return f"{self.cityname}"


class UserManager(models.Manager):

    def get_by_usertypes(self, type):
        return self.filter(isdeleted=False, usertype_id=type)

    def get_by_email(self, email):
        return self.get(isdeleted=False, email=email)

    def get_queryset(self):
        return super().get_queryset().filter(isdeleted=False)


class Users(AbstractUser):
    company_name = models.CharField(default='', max_length=250)
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
    country = models.CharField(
        default='',
        max_length=50,
        blank=True,
        null=True
    )
    state = models.CharField(
        default='',
        max_length=50,
        blank=True,
        null=True
    )
    city = models.CharField(
        default='',
        max_length=50,
        blank=True,
        null=True
    )
    isdeleted = models.BooleanField(default=False)
    createddate = models.DateTimeField(default=utils.timezone.now, blank=True)
    updateddate = models.DateTimeField(blank=True, null=True)

    objects = UserManager()

    class Meta:
        db_table = 'auth_user'
        verbose_name = 'User'
        verbose_name_plural = 'User'

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


class Site(models.Model):
    owner_user = models.ForeignKey(
        Users,
        related_name="siteowner",
        on_delete=models.CASCADE
    )
    sitename = models.CharField(max_length=200)
    address = models.TextField(
        default='',
        blank=True,
        null=True
    )
    country = models.CharField(
        default='',
        max_length=50,
        blank=True,
        null=True
    )
    state = models.CharField(
        default='',
        max_length=50,
        blank=True,
        null=True
    )
    city = models.CharField(
        default='',
        max_length=50,
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
        verbose_name_plural = 'Site'

    def __str__(self):
        return f"{self.sitename}"


class Employee(models.Model):
    user = models.OneToOneField(
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
    joiningdate = models.DateField(null=True)
    min_wages = models.FloatField(default=0.0)
    qualification = models.CharField(default='', max_length=250)
    is_on_leave = models.BooleanField(default=False)
    isdeleted = models.BooleanField(default=False)
    createddate = models.DateTimeField(default=utils.timezone.now, blank=True)
    updateddate = models.DateTimeField(null=True)

    class Meta:
        db_table = 'employee'
        verbose_name = 'Employee'
        verbose_name_plural = 'Employee'

    def __str__(self):
        return f"{self.user.username}"


class Attendance(models.Model):
    employee = models.ForeignKey(
        Employee,
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
        max_length=2,
        choices=(
            ('P', 'Present'),
            ('A', 'Absent'),
            ('HD', 'Half_day'),
            ('OT', 'Over_time')
        ),
        null=True,
        blank=True
    )
    date = models.DateField(null=True)
    isdeleted = models.BooleanField(default=False)
    createddate = models.DateTimeField(default=utils.timezone.now, blank=True)
    updateddate = models.DateTimeField(null=True)

    class Meta:
        db_table = 'attendance'
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance'

    def __str__(self):
        return f"{self.employee}"


class Leave(models.Model):
    employee = models.ForeignKey(
        Employee,
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

    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    reason = models.TextField(blank=True, null=True)
    isdeleted = models.BooleanField(default=False)
    createddate = models.DateTimeField(default=utils.timezone.now, blank=True)
    updateddate = models.DateTimeField(null=True)

    class Meta:
        db_table = 'leave'
        verbose_name = 'Leave'
        verbose_name_plural = 'Leave'

    def __str__(self):
        return f"{self.employee.id}"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
