from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Product, CartItem
from .serializers import ProductSerializer, CartItemSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_permissions(self):
        # Allow anyone to read products, but only admins to modify
        if self.action in ['list', 'retrieve']:
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

class CartViewSet(viewsets.ModelViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(user=self.request.user)

    def get_permissions(self):
        # Require authentication for all cart actions
        return [permissions.IsAuthenticated()]

    @action(detail=False, methods=['GET'])
    def current_cart(self, request):
        cart_items = self.get_queryset()
        serializer = self.get_serializer(cart_items, many=True)
        total = sum(item.total_price for item in cart_items)
        return Response({
            'items': serializer.data,
            'total': total
        })