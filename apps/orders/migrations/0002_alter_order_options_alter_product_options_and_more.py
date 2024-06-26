# Generated by Django 5.0.6 on 2024-05-30 21:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Pedido', 'verbose_name_plural': 'Pedidos'},
        ),
        migrations.AlterModelOptions(
            name='product',
            options={'verbose_name': 'Produto', 'verbose_name_plural': 'Produtos'},
        ),
        migrations.AlterModelOptions(
            name='table',
            options={'verbose_name': 'Mesa', 'verbose_name_plural': 'Mesas'},
        ),
        migrations.CreateModel(
            name='OrderProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantidade', models.PositiveIntegerField(default=1)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.order')),
                ('produto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='orders.product')),
            ],
            options={
                'verbose_name': 'Item do Pedido',
                'verbose_name_plural': 'Itens do Pedido',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='products',
            field=models.ManyToManyField(related_name='orders', through='orders.OrderProduct', to='orders.product'),
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
