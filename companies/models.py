from django.db import models
from django.utils.text import slugify

from backend.image_utils import convert_to_webp

SLUG_HELP = (
    'Name used in the website address, e.g. /products?company=tynor. '
    'Filled in automatically from the name; changing it later breaks old links.'
)


def unique_slug(name, queryset, fallback):
    """Web-address name from `name`, unique within `queryset`."""
    base = slugify(name)[:110].strip('-') or fallback
    slug = base
    counter = 2
    while queryset.filter(slug=slug).exists():
        slug = f'{base}-{counter}'
        counter += 1
    return slug

# Create your models here.
class Company(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=120, unique=True, blank=True, help_text=SLUG_HELP)
    description=models.TextField(blank=True)
    logo=models.ImageField(
        upload_to='company_logos/',
        blank=True,
        help_text='Brand logo shown on the home page. A PNG with a transparent background works best, around 400 x 200 px.',
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = unique_slug(self.name, Company.objects.exclude(pk=self.pk), 'brand')
        convert_to_webp(self.logo)
        super().save(*args, **kwargs)


class CompanyLine(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE, related_name='lines')
    name=models.CharField(max_length=100)
    slug=models.SlugField(max_length=120, blank=True, help_text=SLUG_HELP)
    description=models.TextField(blank=True)
    is_active=models.BooleanField(default=True)
    display_order=models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']
        constraints = [
            models.UniqueConstraint(
                fields=['company', 'name'],
                name='unique_company_line_name'
            ),
            # Line web-address names only need to be unique within a brand
            models.UniqueConstraint(
                fields=['company', 'slug'],
                name='unique_company_line_slug'
            ),
        ]

    def __str__(self):
        return f'{self.company.name} - {self.name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            siblings = CompanyLine.objects.filter(company_id=self.company_id).exclude(pk=self.pk)
            self.slug = unique_slug(self.name, siblings, 'line')
        super().save(*args, **kwargs)
    
