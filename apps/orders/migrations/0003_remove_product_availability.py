# Generated by Django 5.0.6 on 2024-05-30 21:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_options_alter_product_options_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='availability',
        ),
    ]
