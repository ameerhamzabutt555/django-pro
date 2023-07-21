# Generated by Django 4.2 on 2023-07-20 19:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("myapp", "0016_alter_store_stock_inward_id"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="store",
            name="stock_inward_id",
        ),
        migrations.AddField(
            model_name="stockinward",
            name="store_id",
            field=models.ForeignKey(
                null=True, on_delete=django.db.models.deletion.CASCADE, to="myapp.store"
            ),
        ),
    ]
