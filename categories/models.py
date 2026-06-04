from django.db import models

from companies.models import Company    

# Create your models here.
class Category(models.Model):
    name=models.CharField(max_length=100)
    slug=models.SlugField(unique=True)
    company=models.ForeignKey(Company, on_delete=models.CASCADE,null=True, blank=True)


    def __str__(self):
        return self.name