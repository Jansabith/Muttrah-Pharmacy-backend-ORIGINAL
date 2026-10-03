from django.db import models
from django.utils.text import slugify

from backend.image_utils import convert_to_webp, is_new_upload
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

    @property
    def display_title(self):
        """Brand + name, e.g. "TYNOR Knee Cap Air". The brand is left out when
        the name already starts with it ("Tynor Knee Cap" stays as it is)."""
        brand = self.company.name.strip() if self.company_id else ''
        name = self.name.strip()
        if not brand or name.lower() == brand.lower() or name.lower().startswith(f'{brand.lower()} '):
            return name
        return f'{brand} {name}'

    @property
    def image_alt(self):
        """Automatic alt text for the main image, e.g.
        "TYNOR Knee Cap Air – Knee Supports"."""
        category = self.category.name.strip() if self.category_id else ''
        return f'{self.display_title} – {category}' if category else self.display_title

    def image_file_stem(self, suffix=''):
        """SEO-friendly file name for uploaded images, e.g. "tynor-knee-cap-air"
        (whatever the file was called on the computer)."""
        stem = slugify(self.display_title)[:60].strip('-') or 'product'
        return f'{stem}{suffix}'

    def save(self, *args, **kwargs):
        if is_new_upload(self.image):
            convert_to_webp(self.image, filename=self.image_file_stem())
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
    alt_text = models.CharField(
        'Alt text',
        max_length=160,
        blank=True,
        help_text='Optional. What this photo shows, e.g. "TYNOR Knee Cap Air side view". '
                  'Leave empty to use the brand and product name.'
    )

    @property
    def alt(self):
        return self.alt_text.strip() or self.product.display_title

    def save(self, *args, **kwargs):
        if is_new_upload(self.image):
            # Main image is "...", gallery photos continue as "...-2", "...-3"
            position = ProductImage.objects.filter(product_id=self.product_id).exclude(pk=self.pk).count() + 2
            convert_to_webp(self.image, filename=self.product.image_file_stem(f'-{position}'))
        super().save(*args, **kwargs)
    


    



     
