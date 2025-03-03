# Django E-commerce Project Setup Steps

## 1. Project Scaffolding & Initial Setup

### Goal: Create a new Django project and configure basic settings

### Steps:

- Created new Django project using `django-admin startproject djangoEcommerce`
- Configured basic settings in `settings.py`:
  - Added 'rest_framework' and 'corsheaders' to INSTALLED_APPS
  - Set DEBUG = True for development environment only
  - Added 'localhost:3000' and '127.0.0.1:3000' to CORS_ALLOWED_ORIGINS for frontend development
  - Configured SQLite3 database settings for local development
  - Added security settings like SECRET_KEY and ALLOWED_HOSTS
- Set up REST framework and CORS headers:
  - Installed required packages: `pip install djangorestframework django-cors-headers`
  - Added packages with version numbers to requirements.txt
  - Added 'corsheaders.middleware.CorsMiddleware' to MIDDLEWARE before CommonMiddleware
  - Configured CORS settings for frontend access
- Implemented health check API endpoint:
  - Created api/views.py with health_check view function
  - Returns 200 OK status with timestamp to verify API is running
  - Added basic metrics like uptime and system status
- Added API gateway routing:
  - Created api/urls.py for centralized API route management
  - Added 'api/v1/' URL prefix in main urls.py for versioning
  - Set up DefaultRouter for automatic REST endpoint registration
  - Added URL patterns for auth endpoints

## 2. Django Admin Configuration

### Goal: Configure Django's admin interface for managing products and categories

Django Admin is a powerful built-in feature that provides a sophisticated automatic admin interface for managing your application's data. It reads metadata from your models to provide a quick, model-centric interface where trusted users can manage content on your site.

Key Features:

- Automatic CRUD interface for all registered models
- Robust user authentication and granular permissions system
- Comprehensive form validation and data processing
- Detailed change history and audit logging capabilities
- Highly customizable appearance and functionality
- Search and filtering capabilities
- Bulk actions for efficient data management

### Steps:

- Enabled Django's built-in admin interface at /admin URL by:
  - Adding 'django.contrib.admin' to INSTALLED_APPS in settings.py
  - Including admin URLs with path('admin/', admin.site.urls) in main urls.py
  - Running migrations with python manage.py migrate to set up auth tables
  - Creating initial superuser for admin access
- Customized admin site appearance by modifying admin.py:
  - Added `admin.site.site_header = 'E-Commerce Administration'`
  - Added `admin.site.site_title = 'E-Commerce Admin Portal'`
  - Added `admin.site.index_title = 'Welcome to E-Commerce Admin Portal'`
  - Customized CSS for improved visual design
  - Added company logo and branding elements
- Registered models with admin interface by:

  - Creating @admin.register(Category) class CategoryAdmin in products/admin.py:

    - list_display = ['name', 'product_count', 'created_at', 'updated_at']
    - search_fields = ['name', 'description'] for quick lookups
    - prepopulated_fields = {'slug': ('name',)} for automatic slug generation
    - readonly_fields = ['created_at', 'updated_at'] to prevent modification
    - Added product_count method to display number of related products
    - Added list_filter for category filtering
    - Customized form layout using fieldsets

  - Creating @admin.register(Product) class ProductAdmin in products/admin.py:
    - list_display = ['name', 'category', 'price_display', 'stock', 'available', 'created_at']
    - list_filter = ['available', 'category', 'created_at'] for easy filtering
    - list_editable = ['stock', 'available'] for quick updates
    - search_fields = ['name', 'description'] for product search
    - prepopulated_fields = {'slug': ('name',)} for SEO-friendly URLs
    - readonly_fields = ['created_at', 'updated_at']
    - Organized fields into logical fieldsets:
      - Basic Information (name, slug, category, description)
      - Pricing and Inventory (price, stock, available)
      - Metadata (created_at, updated_at) in collapsible section
    - Added price_display method with green formatting and $ symbol
    - Added validation for minimum price and stock values
    - Included image preview functionality

- Access admin interface:
  1. Create superuser: `python manage.py createsuperuser`
     - Enter username, email, and strong password
     - Store credentials securely
  2. Run development server: `python manage.py runserver`
  3. Visit http://localhost:8000/admin
  4. Log in with superuser credentials
  5. Manage products, categories, and other site content
  6. Monitor user activity and changes

## 3. Serializers and Views for API app

### Goal: Create Serializers and Views for API app. Serializers are for transforming data between different formats, for example from JSON to Python objects and vice versa. Views are for handling API requests and responses.

### Steps:

- Create Serializers (api/serializers.py)

```
    from rest_framework import serializers
    from products.models import Category, Product

    # Category Serializer
    class CategorySerializer(serializers.ModelSerializer):
        product_count = serializers.IntegerField(read_only=True)

        class Meta:
            model = Category
            fields = ['id', 'name', 'slug', 'description', 'product_count', 'created_at', 'updated_at']
            read_only_fields = ['created_at', 'updated_at']

    # Product Serializer
    class ProductSerializer(serializers.ModelSerializer):
        category_name = serializers.CharField(source='category.name', read_only=True)

        class Meta:
            model = Product
            fields = ['id', 'name', 'slug', 'category', 'category_name', 'description',
                    'price', 'stock', 'available', 'created_at', 'updated_at']
            read_only_fields = ['created_at', 'updated_at']
```

- Create ViewSets (api/views.py)

```
    from rest_framework import viewsets, filters
    from .serializers import CategorySerializer, ProductSerializer

    class CategoryViewSet(viewsets.ModelViewSet):
        queryset = Category.objects.annotate(product_count=Count('products'))
        serializer_class = CategorySerializer
        lookup_field = 'slug'
        # ... other configurations ...

    class ProductViewSet(viewsets.ModelViewSet):
        queryset = Product.objects.all()
        serializer_class = ProductSerializer
        lookup_field = 'slug'
    # ... other configurations ...
```

- Register URLs (api/urls.py)

```
    from rest_framework import routers

    router = routers.DefaultRouter()
    router.register(r'categories', views.CategoryViewSet)
    router.register(r'products', views.ProductViewSet)

    urlpatterns = [
        path('', include(router.urls)),
        # ... other urls ...
    ]

```

- Configure REST framework settings (djangoEcommerce/settings.py)

```
    REST_FRAMEWORK = {
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
    # ... other settings ...
}

```

## 4. Swagger API Documentation

### Goal: Create Swagger API documentation for the API app. Swagger is a tool that allows you to describe, produce, consume, and visualize RESTful web services.

### Steps:

- Install required packages: `pip install drf-yasg`
- Add 'rest_framework_simplejwt' to INSTALLED_APPS in settings.py
- Configure JWT settings in settings.py:

```



```
