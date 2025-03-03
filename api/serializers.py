from rest_framework import serializers
from products.models import Category, Product

# Serializer for Category model
class CategorySerializer(serializers.ModelSerializer):
    # Add computed field for number of products in category
    product_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Category
        # Define fields to include in serialized output
        fields = ['id', 'name', 'slug', 'description', 'product_count', 'created_at', 'updated_at']
        # Specify fields that should not be modifiable via API
        read_only_fields = ['created_at', 'updated_at']

# Serializer for Product model 
class ProductSerializer(serializers.ModelSerializer):
    # Add field to display category name, sourced from related category object
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        # Define fields to include in serialized output
        fields = [
            'id', 'name', 'slug', 'category', 'category_name',
            'description', 'price', 'stock', 'available',
            'created_at', 'updated_at'
        ]
        # Specify fields that should not be modifiable via API
        read_only_fields = ['created_at', 'updated_at']