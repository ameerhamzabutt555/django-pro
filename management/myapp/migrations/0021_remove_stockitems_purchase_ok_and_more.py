# Generated by Django 4.2 on 2023-08-09 20:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0020_stockitems_total_quantity"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="stockitems",
            name="purchase_ok",
        ),
        migrations.RemoveField(
            model_name="stockitems",
            name="sale_ok",
        ),
    ]
