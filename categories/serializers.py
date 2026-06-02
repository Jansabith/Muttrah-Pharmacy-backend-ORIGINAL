from rest_framework import Serializers
from .models import Category


class CategorySerializer(Serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'

