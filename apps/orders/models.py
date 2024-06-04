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
        default=Status.OPEN
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
    type = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'


class Kitchen(BaseModel):
    class Status(models.TextChoices):
        PREPARING = 'Preparing', 'Preparando'
        READY = 'Ready', 'Pronto'

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PREPARING,
    )
    order_product = models.OneToOneField('OrderProduct', on_delete=models.CASCADE, related_name='kitchen')
    waiter_order = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        limit_choices_to={'user_type': 'waiter'},
        related_name='kitchen_orders',
        null=True,
        blank=True
    )
    started_at = models.DateTimeField(auto_now_add=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Kitchen Order {self.order_product.id} - {self.order_product.product.name}'

    def save(self, *args, **kwargs):
        if self.pk is None and not self.order_product.product.type:
            raise ValidationError('O produto não requer preparação na cozinha.')
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Cozinha'
        verbose_name_plural = 'Cozinhas'


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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.product.type and not hasattr(self, 'kitchen'):
            Kitchen.objects.create(order_product=self, waiter_order=self.order.waiter)

    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'

    def __str__(self):
        return f'{self.product.name} - Quantidade: {self.quantity}'


class Bill(BaseModel):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('paid', 'Paga')
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='bill')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=7, choices=STATUS_CHOICES, default='pending')

    class Meta:
        verbose_name = 'Conta'
        verbose_name_plural = 'Contas'

    def __str__(self):
        return (f'Conta para o Pedido '
                f'{self.order.id} - Total: {self.total_amount} - '
                f'Status: {self.get_status_display()}')
