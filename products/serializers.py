from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    company_name = serializers.CharField(
        source="company.name",
        read_only=True
    )

    category_name = serializers.CharField(
        source="category.name",
        read_only=True
    )

    company_line_name = serializers.CharField(
        source="company_line.name",
        read_only=True
    )

    class Meta:
        model = Product
        fields = "__all__"
