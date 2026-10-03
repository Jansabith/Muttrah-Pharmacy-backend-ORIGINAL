from rest_framework import serializers
from .models import Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    # The editor's alt text, or brand + product name when it is empty
    alt = serializers.CharField(read_only=True)

    class Meta:
        model = ProductImage
        fields = ["id", "image", "alt"]


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

    gallery = ProductImageSerializer(
        many=True,
        read_only=True
    )

    # Automatic main image alt text, e.g. "TYNOR Knee Cap Air – Knee Supports"
    image_alt = serializers.CharField(read_only=True)

    class Meta:
        model = Product
        fields = "__all__"
