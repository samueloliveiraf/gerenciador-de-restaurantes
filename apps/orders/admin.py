from django.contrib import admin
from .models import Table, Product, Order, OrderItem


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'status', 'capacity')
    list_filter = ('status',)
    search_fields = ('number',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'availability')
    list_filter = ('availability',)
    search_fields = ('name', 'description')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'table', 'waiter', 'status', 'datetime')
    list_filter = ('status', 'datetime', 'waiter')
    search_fields = ('table__number', 'waiter__username')
    date_hierarchy = 'datetime'

    def get_waiter_username(self, obj):
        return obj.waiter.username
    get_waiter_username.admin_order_field = 'waiter'
    get_waiter_username.short_description = 'Waiter Username'


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('order', 'product', 'quantity')
    list_filter = ('order', 'product')
    search_fields = ('order__id', 'product__name')
