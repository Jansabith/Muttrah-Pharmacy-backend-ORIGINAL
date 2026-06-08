from django.db import models

# Create your models here.
class Company(models.Model):
    name=models.CharField(max_length=100)
    description=models.TextField(blank=True)

    def __str__(self):
        return self.name


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
    
