# Generated by Django 4.2.3 on 2023-07-18 11:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0013_rename_ref_id_expenses_ref_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="stockitems",
            name="purchase_ok",
            field=models.BooleanField(default=True, verbose_name="Can be Purchased"),
        ),
        migrations.AddField(
            model_name="stockitems",
            name="sale_ok",
            field=models.BooleanField(default=True, verbose_name="Can be Sold"),
        ),
    ]
