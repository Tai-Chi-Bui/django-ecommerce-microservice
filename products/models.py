from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator

# Models for the products app

class Category(models.Model):
    # Name of the category, must be unique
    name = models.CharField(max_length=100, unique=True)
    # URL-friendly version of the name, auto-generated from name field
    slug = models.SlugField(max_length=100, unique=True)
    # Optional description of the category
    description = models.TextField(blank=True)
    # Timestamp for when category was created
    created_at = models.DateTimeField(auto_now_add=True)
    # Timestamp for when category was last updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Customize model metadata for admin interface
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        # Sort categories by name by default
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        # Auto-generate slug from name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        # String representation of category
        return self.name


class Product(models.Model):
    # Product name
    name = models.CharField(max_length=200)
    # URL-friendly version of name, can be blank (auto-generated)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    # Foreign key relationship to Category model, deletes products if category is deleted
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    # Detailed product description
    description = models.TextField()
    # Product price with validation to ensure minimum price of 0.01
    price = models.DecimalField(
        max_digits=10, 
        decimal_places=2,
        validators=[MinValueValidator(0.01)]
    )
    # Current inventory level
    stock = models.PositiveIntegerField(default=0)
    # Whether product is currently available for purchase
    available = models.BooleanField(default=True)
    # Timestamp when product was created
    created_at = models.DateTimeField(auto_now_add=True)
    # Timestamp when product was last updated
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        # Sort products by name by default
        ordering = ['name']

    def save(self, *args, **kwargs):
        # Auto-generate slug from name if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        # String representation of product
        return self.name
