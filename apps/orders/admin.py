from django.contrib import admin
from django import forms
from .models import Table, Product, Order, OrderProduct


class OrderProductInline(admin.TabularInline):
    model = OrderProduct
    extra = 1


class OrderForm(forms.ModelForm):
    products = forms.ModelMultipleChoiceField(queryset=Product.objects.all(), widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Order
        fields = '__all__'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    inlines = (OrderProductInline,)
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
