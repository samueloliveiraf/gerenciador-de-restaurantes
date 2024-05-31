from django.core.exceptions import ValidationError
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
    datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Pedido {self.id} - Mesa {self.table.number}'

    def clean(self):
        if not self.pk and self.table.status != Table.Status.CLOSED:
            raise ValidationError(f'A mesa {self.table.number} não está fechada. Não é possível criar um novo pedido.')
        super().clean()

    class Meta:
        verbose_name = 'Pedido'
        verbose_name_plural = 'Pedidos'


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_products')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'

    def __str__(self):
        return f'{self.product.name} - Quantidade: {self.quantity}'


class Bill(BaseModel):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='bill')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    generated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'

    def __str__(self):
        return f'Conta para o Pedido {self.order.id} - Total: {self.total_amount}'
