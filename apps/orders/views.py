from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from .models import Order, OrderProduct, Table, Bill
from .serializers import OrderSerializer, AddOrderProductSerializer, CanFinalizeOrderPermission


class CreateOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            order = serializer.save()
            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AddProductToOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, order_id, *args, **kwargs):
        try:
            Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Pedido não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = AddOrderProductSerializer(data=request.data, context={'order_id': order_id})
        if serializer.is_valid():
            order_product = serializer.save()
            return Response(AddOrderProductSerializer(order_product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RemoveProductFromOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def delete(self, request, order_id, product_id, *args, **kwargs):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Pedido não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        order_products = OrderProduct.objects.filter(order=order, product_id=product_id)
        if not order_products.exists():
            return Response({'error': 'Produto não encontrado no pedido.'}, status=status.HTTP_404_NOT_FOUND)

        order_products.delete()
        return Response({'success': 'Produto removido do pedido.'}, status=status.HTTP_204_NO_CONTENT)


class FinalizeOrderView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, CanFinalizeOrderPermission]

    def post(self, request, order_id, *args, **kwargs):
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response({'error': 'Pedido não encontrado.'}, status=status.HTTP_404_NOT_FOUND)

        table = order.table

        table.status = Table.Status.OPEN
        table.save()

        total_amount = sum(item.product.price * item.quantity for item in order.order_products.all())
        Bill.objects.create(order=order, total_amount=total_amount)

        return Response({'success': 'Pedido finalizado e conta gerada com sucesso.'}, status=status.HTTP_200_OK)
