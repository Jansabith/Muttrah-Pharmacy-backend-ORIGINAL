from django.db import models

from categories.models import Category
from companies.models import Company, CompanyLine

# Create your models here.
class Product(models.Model):
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    company=models.ForeignKey(Company, on_delete=models.CASCADE)
    company_line=models.ForeignKey(
        CompanyLine,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='products'
    )
    name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True)
    description=models.TextField()
    size=models.CharField(
        max_length=255,
        blank=True,
        help_text='Enter sizes separated by commas, for example: S, M, L, XL'
    )
    image=models.ImageField(upload_to='products/')

    meta_title = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="SEO Meta Title (max 60-70 characters)"
    )
    meta_description = models.TextField(
        blank=True,
        null=True,
        help_text="SEO Meta Description (max 150-160 characters)"
    )
    meta_keywords = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text="SEO Meta Keywords (comma-separated)"
    )

    is_available=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
class ProductSize(models.Model):
    product=models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sizes')
    size_name=models.CharField(max_length=100)


class ProductImage(models.Model):

    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='gallery'
    )

    image = models.ImageField(
        upload_to='gallery/'
    )
    


    



     
