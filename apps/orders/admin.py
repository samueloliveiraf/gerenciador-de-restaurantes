from django.contrib import admin
from django import forms

from .models import Table, Product, Order, OrderProduct, Bill


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['table'].queryset = Table.objects.filter(status=Table.Status.CLOSED)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    inlines = [OrderProductInline]
    list_display = ('id', 'table', 'waiter', 'status', 'datetime')
    list_filter = ('status', 'datetime', 'waiter')
    search_fields = ('table__number', 'waiter__username')
    date_hierarchy = 'datetime'

    def get_waiter_username(self, obj):
        return obj.waiter.username
    get_waiter_username.admin_order_field = 'waiter'
    get_waiter_username.short_description = 'Waiter Username'


@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ('number', 'status', 'capacity')
    list_filter = ('status',)
    search_fields = ('number',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price')
    search_fields = ('name', 'description')


admin.site.register(Bill)
