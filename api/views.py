from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.db.models import Count
from products.models import Category, Product
from .serializers import CategorySerializer, ProductSerializer

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response(
        {"status": "healthy"},
        status=status.HTTP_200_OK
    )

class CategoryViewSet(viewsets.ModelViewSet):
    # Define base queryset that annotates each category with its product count
    queryset = Category.objects.annotate(
        product_count=Count('products')  # Count products related to each category
    )
    
    # Specify serializer class to handle data transformation
    serializer_class = CategorySerializer
    
    # Allow read access to all, but require authentication for write operations
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Enable search and ordering functionality
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
    # Fields that can be searched
    search_fields = ['name', 'description']
    
    # Fields that can be used for ordering results
    ordering_fields = ['name', 'created_at']
    
    # Use slug instead of id for lookups in URLs
    lookup_field = 'slug'

class ProductViewSet(viewsets.ModelViewSet):
    # Base queryset for all products
    queryset = Product.objects.all()
    
    # Specify serializer class to handle data transformation
    serializer_class = ProductSerializer
    
    # Allow read access to all, but require authentication for write operations
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Enable search and ordering functionality
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    
    # Fields that can be searched - includes product name, description and category name
    search_fields = ['name', 'description', 'category__name']
    
    # Fields that can be used for ordering results
    ordering_fields = ['name', 'price', 'created_at']
    
    # Use slug instead of id for lookups in URLs
    lookup_field = 'slug'

    def get_queryset(self):
        """
        Optionally filters products by category slug from query parameters.
        Example: /api/products/?category=electronics
        """
        queryset = Product.objects.all()
        category_slug = self.request.query_params.get('category', None)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        return queryset