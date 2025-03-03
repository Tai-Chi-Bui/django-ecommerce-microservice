from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product

# Register the Category model with the Django admin site
# This decorator is equivalent to calling admin.site.register(Category, CategoryAdmin)
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'product_count', 'created_at', 'updated_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']

    def product_count(self, obj):
        return obj.products.count()
    product_count.short_description = 'Number of Products'

# Register the Product model with the Django admin site
# This decorator is equivalent to calling admin.site.register(Product, ProductAdmin)
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price_display', 'stock', 'available', 'created_at']
    list_filter = ['available', 'category', 'created_at']
    list_editable = ['stock', 'available']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Pricing and Inventory', {
            'fields': ('price', 'stock', 'available')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def price_display(self, obj):
        # Format price with 2 decimal places to ensure consistent display
        return format_html('<span style="color: green;">${:.2f}</span>', float(obj.price))
    price_display.short_description = 'Price'
