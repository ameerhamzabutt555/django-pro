# Generated by Django 4.1.7 on 2023-07-16 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0007_expenses'),
    ]

    operations = [
        migrations.AddField(
            model_name='expenses',
            name='invoice_number',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
