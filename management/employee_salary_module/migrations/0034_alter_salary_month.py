# Generated by Django 4.2 on 2023-08-09 22:20

from django.db import migrations
import django.utils.timezone
import month.models


class Migration(migrations.Migration):

    dependencies = [
        (
            "employee_salary_module",
            "0033_employee_address_employee_cnic_number_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="salary",
            name="month",
            field=month.models.MonthField(default=django.utils.timezone.now),
        ),
    ]
