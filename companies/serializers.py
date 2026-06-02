from rest_framework import serializers
from .models import Category        

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'    

