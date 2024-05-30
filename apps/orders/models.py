from django.db import models

from apps.core.models import BaseModel
from apps.users.models import User


class Table(BaseModel):
    class Status(models.TextChoices):
        CANCELLED = 'Cancelled', 'Cancelada'
        CLOSED = 'Closed', 'Fechada'
        OPEN = 'Open', 'Aberta'

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.CLOSED
    )
    number = models.PositiveIntegerField(unique=True)
    capacity = models.PositiveIntegerField()

    def __str__(self):
        return f'Mesa {self.number} (Capacidade: {self.capacity})'

    class Meta:
        verbose_name = 'Mesa'
        verbose_name_plural = 'Mesas'


class Product(BaseModel):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'


class Order(BaseModel):
    class Status(models.TextChoices):
        ACCOMPLISHED = 'accomplished', 'Realizado'
        PREPARATION = 'Preparation', 'Preparando'
        CANCELLED = 'Cancelled', 'Cancelado'
        READY = 'Ready', 'Pronto'

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACCOMPLISHED,
    )
    table = models.ForeignKey(Table, on_delete=models.CASCADE, related_name='orders')
    waiter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'user_type': 'waiter'},
        related_name='orders'
    )
    products = models.ManyToManyField(Product, related_name='orders', through='OrderProduct')
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pedido {self.id} - Mesa {self.table.number}'

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'


class OrderProduct(models.Model):
    pedido = models.ForeignKey(Order, on_delete=models.CASCADE)
    produto = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f'{self.produto.name} - Quantidade: {self.quantidade}'

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'
