# Generated by Django 4.2 on 2023-07-20 18:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0015_remove_stockinward_store_id_store_stock_inward_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="store",
            name="stock_inward_id",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="myapp.stockinward",
            ),
        ),
    ]
