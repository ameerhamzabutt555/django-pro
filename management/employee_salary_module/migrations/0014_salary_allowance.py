# Generated by Django 4.2 on 2023-08-02 23:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "employee_salary_module",
            "0013_alter_salary_basic_salary_alter_salary_overtime_pay_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="salary",
            name="allowance",
            field=models.FloatField(default=0),
        ),
    ]
