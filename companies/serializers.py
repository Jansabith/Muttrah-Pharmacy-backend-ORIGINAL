from rest_framework import serializers
from .models import Company, CompanyLine


class CompanyLineSerializer(serializers.ModelSerializer):
    class Meta:
        model=CompanyLine
        fields='__all__'

class CompanySerializer(serializers.ModelSerializer):
    lines=CompanyLineSerializer(many=True, read_only=True)

    class Meta:
        model=Company
        fields='__all__'    
