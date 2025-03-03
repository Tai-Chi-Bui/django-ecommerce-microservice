from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
# Register your API routes here
# Example: router.register(r'products', views.ProductViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('auth/', include('rest_framework.urls')),
    path('health/', views.health_check, name='health_check'),
]