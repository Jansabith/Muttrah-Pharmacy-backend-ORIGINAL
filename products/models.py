from django.db import models

from backend.image_utils import convert_to_webp
from categories.models import Category
from companies.models import Company, CompanyLine

class ProductQuerySet(models.QuerySet):
    def with_main_image(self):
        """Products the website may show: a product imported from Excel stays
        hidden until its main image is added in the admin."""
        return self.exclude(image='')


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
    # Optional only so the Excel import can create products before their
    # photos exist; the admin "Add product" form still requires it
    image=models.ImageField(
        'Main image',
        upload_to='products/',
        blank=True,
        help_text='Products without a main image are hidden on the website.'
    )
    youtube_url=models.URLField(
        blank=True,
        help_text='Optional YouTube video link, for example: https://www.youtube.com/watch?v=XXXXXXXXXXX'
    )

    # Column types match SEO columns an earlier (since removed) migration
    # created in some databases, so both old and fresh databases line up.
    meta_title=models.CharField(
        'SEO title',
        max_length=255,
        blank=True,
        null=True,
        help_text='Optional. Title shown in Google results and the browser tab (best under 60 characters). '
                  '" | Muttrah Pharmacy" is added automatically. Leave empty to use the product name.'
    )
    meta_description=models.TextField(
        'SEO description',
        blank=True,
        null=True,
        help_text='Optional. Text shown under the title in Google results (best 120-155 characters). '
                  'Leave empty to use the start of the product description.'
    )

    is_available=models.BooleanField(default=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    objects = ProductQuerySet.as_manager()

    class Meta:
        ordering = ['-created_at', 'id']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        convert_to_webp(self.image)
        super().save(*args, **kwargs)
    

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

    def save(self, *args, **kwargs):
        convert_to_webp(self.image)
        super().save(*args, **kwargs)
    


    



     
