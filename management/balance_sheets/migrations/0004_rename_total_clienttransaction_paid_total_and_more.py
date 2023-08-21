# Generated by Django 4.2 on 2023-08-16 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("balance_sheets", "0003_remove_clienttransaction_month"),
    ]

    operations = [
        migrations.RenameField(
            model_name="clienttransaction",
            old_name="total",
            new_name="paid_total",
        ),
        migrations.AddField(
            model_name="clienttransaction",
            name="price_total",
            field=models.DecimalField(
                blank=True, decimal_places=2, max_digits=10, null=True
            ),
        ),
    ]
