# Generated by Django 4.2 on 2023-08-02 23:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employee_salary_module", "0014_salary_allowance"),
    ]

    operations = [
        migrations.AddField(
            model_name="salary",
            name="total_working_days",
            field=models.FloatField(default=0),
        ),
    ]
