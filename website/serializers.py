from rest_framework import serializers
from .models import (
    AboutPage,
    AboutTimelineItem,
    ContactPage,
    ContactSubmission,
    FooterContent,
    FooterQuickLink,
    FooterSocialLink,
    HomeFeature,
    HomePage,
    HomeTrustItem,
    AboutHeroImage,
)


class HomeFeatureSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeFeature
        fields = ("id", "title", "description", "order")


class HomeTrustItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeTrustItem
        fields = ("id", "title", "order")


class HomePageSerializer(serializers.ModelSerializer):
    features = serializers.SerializerMethodField()
    trust_items = serializers.SerializerMethodField()

    class Meta:
        model = HomePage
        fields = "__all__"

    def get_features(self, obj):
        queryset = obj.features.filter(is_active=True)
        return HomeFeatureSerializer(queryset, many=True).data

    def get_trust_items(self, obj):
        queryset = obj.trust_items.filter(is_active=True)
        return HomeTrustItemSerializer(queryset, many=True).data


class AboutTimelineItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutTimelineItem
        fields = ("id", "title", "description", "order")


class AboutHeroImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutHeroImage
        fields = ("id", "image", "order")


class AboutPageSerializer(serializers.ModelSerializer):
    timeline_items = serializers.SerializerMethodField()
    hero_images = serializers.SerializerMethodField()

    class Meta:
        model = AboutPage
        fields = "__all__"

    def get_timeline_items(self, obj):
        queryset = obj.timeline_items.filter(is_active=True)
        return AboutTimelineItemSerializer(queryset, many=True).data

    def get_hero_images(self, obj):
        queryset = obj.hero_images.filter(is_active=True)
        request = self.context.get("request")
        
        # Build absolute URIs for the images manually or use context
        data = AboutHeroImageSerializer(queryset, many=True, context=self.context).data
        return data


class ContactPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactPage
        fields = "__all__"


class FooterQuickLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterQuickLink
        fields = ("id", "label", "url", "order")


class FooterSocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = FooterSocialLink
        fields = ("id", "label", "url", "order")


class FooterContentSerializer(serializers.ModelSerializer):
    quick_links = serializers.SerializerMethodField()
    social_links = serializers.SerializerMethodField()

    class Meta:
        model = FooterContent
        fields = "__all__"

    def get_quick_links(self, obj):
        queryset = obj.quick_links.filter(is_active=True)
        return FooterQuickLinkSerializer(queryset, many=True).data

    def get_social_links(self, obj):
        queryset = obj.social_links.filter(is_active=True)
        return FooterSocialLinkSerializer(queryset, many=True).data


class ContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactSubmission
        fields = ("id", "name", "email", "phone", "message", "created_at")
        read_only_fields = ("id", "created_at")
