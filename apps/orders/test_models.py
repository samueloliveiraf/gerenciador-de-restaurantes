from django.test import TestCase

from apps.orders.models import Table, Product, Order, OrderItem
from apps.users.models import User


class TableModelTest(TestCase):
    def setUp(self):
        self.table = Table.objects.create(number=1, capacity=4)

    def test_table_creation(self):
        self.assertEqual(self.table.number, 1)
        self.assertEqual(self.table.capacity, 4)
        self.assertEqual(self.table.status, Table.Status.CLOSED)

    def test_table_str(self):
        self.assertEqual(str(self.table), 'Mesa 1 (Capacidade: 4)')


class ProductModelTest(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name='Pizza', price=19.99)

    def test_product_creation(self):
        self.assertEqual(self.product.name, 'Pizza')
        self.assertEqual(self.product.price, 19.99)
        self.assertTrue(self.product.availability)

    def test_product_str(self):
        self.assertEqual(str(self.product), 'Pizza')


class OrderModelTest(TestCase):
    def setUp(self):
        self.table = Table.objects.create(number=2, capacity=4)
        self.waiter = User.objects.create_user(email='test@example.com', password='12345', user_type='waiter')
        self.order = Order.objects.create(table=self.table, waiter=self.waiter)

    def test_order_creation(self):
        self.assertEqual(self.order.table, self.table)
        self.assertEqual(self.order.waiter, self.waiter)
        self.assertEqual(self.order.status, Order.Status.ACCOMPLISHED)
        self.assertTrue(self.order.datetime)

    def test_order_str(self):
        self.assertEqual(str(self.order), f'Pedido {self.order.id} - Mesa {self.table.number}')


class OrderItemModelTest(TestCase):
    def setUp(self):
        self.table = Table.objects.create(number=3, capacity=4)
        self.waiter = User.objects.create_user(email='test@example.com', password='12345', user_type='waiter')
        self.order = Order.objects.create(table=self.table, waiter=self.waiter)
        self.product = Product.objects.create(name='Coke', price=4.99)
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=2)

    def test_order_item_creation(self):
        self.assertEqual(self.order_item.order, self.order)
        self.assertEqual(self.order_item.product, self.product)
        self.assertEqual(self.order_item.quantity, 2)

    def test_order_item_str(self):
        self.assertEqual(str(self.order_item), f'2 x Coke (Pedido {self.order.id})')
