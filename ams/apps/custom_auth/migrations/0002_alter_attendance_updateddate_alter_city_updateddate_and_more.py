# Generated by Django 4.2.16 on 2025-03-06 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('custom_auth', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attendance',
            name='updateddate',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='city',
            name='updateddate',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='country',
            name='updateddate',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='employee',
            name='updateddate',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='leave',
            name='updateddate',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='site',
            name='updateddate',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='state',
            name='updateddate',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='users',
            name='updateddate',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
        migrations.AlterField(
            model_name='usertype',
            name='updateddate',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
