from django.db import transaction
from rest_framework import serializers
from .models import Product, Order, OrderItem

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('name', 'description', 'price', 'stock')
        
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("Price must be greater than zero.")
        return value
    

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    product_price = serializers.DecimalField(source='product.price', max_digits=10, decimal_places=2, read_only=True)
    class Meta:
        model = OrderItem
        fields = ('product_name', 'product_price', 'quantity', 'item_subtotal')


class OrderCreateSerializer(serializers.ModelSerializer):
    class OrderItemCreateSerializer(serializers.ModelSerializer):
        class Meta:
            model = OrderItem
            fields = ('product', 'quantity')

    order_id = serializers.UUIDField(read_only=True)
    items = OrderItemCreateSerializer(many=True, required=False)

    def update(self, instance, validated_data):
        order_items_data = validated_data.pop('items')
        with transaction.atomic():
            instance = super().update(instance, validated_data)
            if order_items_data:
                # clear existing items and create new ones
                instance.items.all().delete()
                for item_data in order_items_data:
                    OrderItem.objects.create(order=instance, **item_data)
        return instance

    def create(self, validated_data):
        Orderitems_data = validated_data.pop('items')
        with transaction.atomic():
            order = Order.objects.create(**validated_data)
            for item in Orderitems_data:
                OrderItem.objects.create(order=order, **item)
        return order

    class Meta:
        model = Order
        fields = ('order_id', 'user', 'status', 'items')
        extra_kwargs = {'user': {'read_only': True}}

class OrderSerializer(serializers.ModelSerializer):
    order_id = serializers.CharField(read_only=True)
    items = OrderItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField()


    def get_total_price(self, obj):
        order_items = obj.items.all()
        return sum(order_item.item_subtotal for order_item in order_items)

    class Meta:
        model = Order
        fields = ('order_id', 'user', 'created_at', 'status', 'items', 'total_price')


class ProductInfoSerializer(serializers.Serializer):
    products = ProductSerializer(many=True)
    count = serializers.IntegerField()
    max_price = serializers.FloatField()
