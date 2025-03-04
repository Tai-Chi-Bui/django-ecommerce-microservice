from rest_framework import viewsets, filters
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status
from django.db.models import Count
from products.models import Category, Product
from .serializers import CategorySerializer, ProductSerializer
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

@api_view(['GET'])
@permission_classes([AllowAny])
def health_check(request):
    return Response(
        {"status": "healthy"},
        status=status.HTTP_200_OK
    )

class CategoryViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing categories.
    """
    queryset = Category.objects.annotate(product_count=Count('products'))
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description']
    ordering_fields = ['name', 'created_at']
    lookup_field = 'slug'

    @swagger_auto_schema(
        operation_description="List all categories",
        manual_parameters=[
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search in name and description",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Order by field (prefix with - for descending)",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

class ProductViewSet(viewsets.ModelViewSet):
    """
    ViewSet for viewing and editing products.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # Enable search and ordering functionality
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category__name']
    
    # Fields that can be used for ordering results
    ordering_fields = ['name', 'price', 'created_at']
    lookup_field = 'slug'

    @swagger_auto_schema(
        operation_description="List all products",
        manual_parameters=[
            openapi.Parameter(
                'category',
                openapi.IN_QUERY,
                description="Filter by category slug",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                'search',
                openapi.IN_QUERY,
                description="Search in name, description and category name",
                type=openapi.TYPE_STRING,
                required=False,
            ),
            openapi.Parameter(
                'ordering',
                openapi.IN_QUERY,
                description="Order by field (prefix with - for descending)",
                type=openapi.TYPE_STRING,
                required=False,
            ),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

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