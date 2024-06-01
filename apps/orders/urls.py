from django.urls import path
from .views import *


urlpatterns = [
    path('create-order/', CreateOrderView.as_view(), name='create-order'),
    path('<str:order_id>/add-product/', AddProductToOrderView.as_view(), name='add-product-to-order'),
    path('<str:order_id>/remove-product/<str:product_id>/', RemoveProductFromOrderView.as_view(), name='remove-product-from-order'),
    path('<str:order_id>/finalize/', FinalizeOrderView.as_view(), name='finalize-order')
]
