# Generated by Django 4.2 on 2023-08-17 20:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        (
            "balance_sheets",
            "0007_alter_clientpayment_balance_alter_clientpayment_paid_and_more",
        ),
    ]

    operations = [
        migrations.AddField(
            model_name="clientbill",
            name="recipient",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
