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
    image=models.ImageField(upload_to='products/')

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
    


    



     
