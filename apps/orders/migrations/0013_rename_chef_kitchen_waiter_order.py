# Generated by Django 5.0.6 on 2024-06-04 23:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0012_alter_table_status'),
    ]

    operations = [
        migrations.RenameField(
            model_name='kitchen',
            old_name='chef',
            new_name='waiter_order',
        ),
    ]
