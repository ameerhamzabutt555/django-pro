# Generated by Django 4.2 on 2023-08-03 00:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("employee_salary_module", "0020_salary_payable_days"),
    ]

    operations = [
        migrations.AddField(
            model_name="salary",
            name="gross_payable",
            field=models.FloatField(default=0),
        ),
    ]
