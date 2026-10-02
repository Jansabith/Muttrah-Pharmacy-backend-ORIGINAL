from django.db import models

from backend.image_utils import convert_to_webp

# Create your models here.
class Company(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    logo=models.ImageField(
        upload_to='company_logos/',
        blank=True,
        help_text='Brand logo shown on the home page. A PNG with a transparent background works best, around 400 x 200 px.',
    )

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        convert_to_webp(self.logo)
        super().save(*args, **kwargs)


class CompanyLine(models.Model):
    company=models.ForeignKey(Company, on_delete=models.CASCADE, related_name='lines')
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)
    is_active=models.BooleanField(default=True)
    display_order=models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['display_order', 'name']
        constraints = [
            models.UniqueConstraint(
                fields=['company', 'name'],
                name='unique_company_line_name'
            )
        ]

    def __str__(self):
        return f'{self.company.name} - {self.name}'
    
