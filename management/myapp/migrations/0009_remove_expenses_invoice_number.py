# Generated by Django 4.1.7 on 2023-07-16 19:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_expenses_invoice_number'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='expenses',
            name='invoice_number',
        ),
    ]
