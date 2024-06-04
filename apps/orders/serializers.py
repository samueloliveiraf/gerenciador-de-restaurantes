from rest_framework.permissions import BasePermission
from rest_framework import serializers

from .models import Order, OrderProduct, Table


class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    order_products = OrderProductSerializer(many=True)

    class Meta:
        model = Order
        fields = ['table', 'order_products']

    def validate(self, data):
        table = data.get('table')
        if table.status != Table.Status.OPEN:
            raise serializers.ValidationError(
                f'A mesa {table.number} não está aberta. Não é possível criar um novo pedido.')
        return data

    def create(self, validated_data):
        order_products_data = validated_data.pop('order_products')
        table = validated_data.get('table')
        waiter = self.context['request'].user

        order = Order.objects.create(waiter=waiter, **validated_data)
        for order_product_data in order_products_data:
            OrderProduct.objects.create(order=order, **order_product_data)

        table.status = Table.Status.CLOSED
        table.save()

        return order


class AddOrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderProduct
        fields = ['product', 'quantity']

    def create(self, validated_data):
        order_id = self.context['order_id']
        order = Order.objects.get(id=order_id)
        order_product = OrderProduct.objects.create(order=order, **validated_data)
        return order_product


class CanFinalizeOrderPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        user = request.user
        return user.user_type in ['admin', 'manager', 'box']
