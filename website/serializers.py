from rest_framework import serializers
from .models import (
    AboutPage,
    AboutTimelineItem,
    ContactPage,
    ContactSubmission,
    HomeFeature,
    HomePage,
)


class HomeFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeFeature
        fields = ("id", "title", "description", "order")


class HomePageSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()

    class Meta:
        model = HomePage
        fields = "__all__"

    def get_features(self, obj):
        queryset = obj.features.filter(is_active=True)
        return HomeFeatureSerializer(queryset, many=True).data


class AboutTimelineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutTimelineItem
        fields = ("id", "title", "description", "order")


class AboutPageSerializer(serializers.ModelSerializer):
    timeline_items = serializers.SerializerMethodField()

    class Meta:
        model = AboutPage
        fields = "__all__"

    def get_timeline_items(self, obj):
        queryset = obj.timeline_items.filter(is_active=True)
        return AboutTimelineItemSerializer(queryset, many=True).data


class ContactPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPage
        fields = "__all__"


class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = ("id", "name", "email", "phone", "message", "created_at")
        read_only_fields = ("id", "created_at")
