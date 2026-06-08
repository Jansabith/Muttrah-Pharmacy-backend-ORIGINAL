from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    company_line_name = serializers.CharField(
        source="company_line.name",
        read_only=True
    )

    class Meta:
        model=Category
        fields='__all__'
