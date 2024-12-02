from django.contrib import admin
from django.utils.html import mark_safe
from .models import Product, CartItem

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'display_thumbnail')
    list_filter = ('category',)
    search_fields = ('name', 'category')
    
    def display_thumbnail(self, obj):
        if obj.thumbnail:
            return mark_safe(f'<img src="{obj.thumbnail.url}" width="100" height="100" />')
        return 'No Thumbnail'
    display_thumbnail.short_description = 'Thumbnail'

@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'total_price')
    list_filter = ('user', 'product__category')
    
    def total_price(self, obj):
        return f"${obj.product.price * obj.quantity:.2f}"
    total_price.short_description = 'Total Price'