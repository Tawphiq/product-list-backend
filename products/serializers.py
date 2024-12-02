from rest_framework import serializers
from .models import Product, CartItem

class ProductSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price', 'image']

    def get_image(self, obj):
        return {
            'thumbnail': obj.thumbnail.url if obj.thumbnail else None,
            'mobile': obj.mobile_image.url if obj.mobile_image else None,
            'tablet': obj.tablet_image.url if obj.tablet_image else None,
            'desktop': obj.desktop_image.url if obj.desktop_image else None
        }

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    product_id = serializers.IntegerField(write_only=True)
    total_price = serializers.DecimalField(max_digits=10, decimal_places=2, read_only=True)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity', 'total_price']

    def create(self, validated_data):
        product_id = validated_data.pop('product_id')
        product = Product.objects.get(id=product_id)
        user = self.context['request'].user
        
        # Check if product already in cart, update quantity if so
        cart_item, created = CartItem.objects.get_or_create(
            user=user, 
            product=product, 
            defaults={'quantity': validated_data.get('quantity', 1)}
        )
        
        if not created:
            cart_item.quantity += validated_data.get('quantity', 1)
            cart_item.save()
        
        return cart_item