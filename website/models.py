from django.core.exceptions import ValidationError
from django.db import models


class SingletonPageModel(models.Model):
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

    @classmethod
    def load(cls):
        obj = cls.objects.first()
        if obj:
            return obj
        return cls.objects.create()

    def clean(self):
        if not self.pk and self.__class__.objects.exists():
            raise ValidationError("Only one page content record is allowed.")

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


class HomePage(SingletonPageModel):
    hero_eyebrow = models.CharField(
        max_length=180,
        default="Pharmaceutical and orthopedic distributor in Oman",
    )
    hero_title = models.CharField(max_length=180, default="Muttrah Pharmacy")
    hero_description = models.TextField(
        default=(
            "A dependable warehouse partner for pharmacies, clinics, hospitals, "
            "and orthopedic teams sourcing quality medical products across Oman."
        )
    )
    primary_button_label = models.CharField(max_length=80, default="Browse Products")
    secondary_button_label = models.CharField(max_length=80, default="Contact Sales")
    intro_eyebrow = models.CharField(max_length=120, default="Company Introduction")
    intro_title = models.CharField(
        max_length=220,
        default="Built for dependable medical product distribution.",
    )
    brands_eyebrow = models.CharField(max_length=120, default="Featured Brands")
    brands_title = models.CharField(
        max_length=220,
        default="Brands represented in the live catalog",
    )
    brands_description = models.TextField(
        default=(
            "Muttrah Pharmacy partners with internationally recognized healthcare and orthopedic "
            "brands to deliver high-quality products and trusted medical solutions across Oman. "
            "Our portfolio includes leading manufacturers specializing in pharmaceuticals, orthopedic "
            "care, rehabilitation, and healthcare supplies."
        )
    )
    categories_eyebrow = models.CharField(max_length=120, default="Product Categories")
    categories_title = models.CharField(max_length=220, default="Organized for fast sourcing")
    trust_eyebrow = models.CharField(max_length=120, default="Why Choose Us")
    trust_title = models.CharField(
        max_length=220,
        default="Why Healthcare Professionals Trust Muttrah Pharmacy",
    )
    cta_eyebrow = models.CharField(max_length=120, default="Ready to source")
    cta_title = models.CharField(max_length=220, default="Connect with Muttrah Pharmacy today.")
    cta_button_label = models.CharField(max_length=80, default="Send Inquiry")

    class Meta:
        verbose_name = "Home Page Content"
        verbose_name_plural = "Home Page Content"

    def __str__(self):
        return "Home Page Content"


class HomeFeature(models.Model):
    home_page = models.ForeignKey(
        HomePage,
        on_delete=models.CASCADE,
        related_name="features",
    )
    title = models.CharField(max_length=160)
    description = models.TextField(
        default=(
            "A practical operating model for procurement teams that need clear "
            "catalog access and fast communication."
        )
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class HomeTrustItem(models.Model):
    home_page = models.ForeignKey(
        HomePage,
        on_delete=models.CASCADE,
        related_name="trust_items",
    )
    title = models.CharField(max_length=180)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class AboutPage(SingletonPageModel):
    eyebrow = models.CharField(max_length=120, default="About Us")
    title = models.CharField(
        max_length=240,
        default="A professional distribution and warehouse partner in Oman.",
    )
    overview = models.TextField(
        default=(
            "Muttrah Pharmacy supports healthcare procurement teams with a focused "
            "catalog of pharmaceutical, orthopedic, and medical supply products."
        )
    )
    mission_title = models.CharField(max_length=220, default="Mission")
    mission_text = models.TextField(
        default="Make critical product sourcing clear, reliable, and responsive."
    )
    vision_title = models.CharField(max_length=220, default="Vision")
    vision_text = models.TextField(
        default="Become a leading medical distribution reference for Oman."
    )
    warehouse_title = models.CharField(max_length=180, default="Warehouse Information")
    warehouse_text = models.TextField(
        default="Organized product storage and catalog-backed distribution readiness."
    )
    network_title = models.CharField(max_length=180, default="Distribution Network")
    network_text = models.TextField(
        default="Supply support for pharmacies, clinics, hospitals, and orthopedic providers."
    )
    why_title = models.CharField(max_length=180, default="Why Choose Us")
    why_text = models.TextField(
        default="Focused medical category knowledge with direct inquiry channels."
    )
    brands_eyebrow = models.CharField(max_length=120, default="Brands We Represent")
    brands_title = models.CharField(
        max_length=220,
        default="Company data loaded from the API",
    )
    timeline_eyebrow = models.CharField(max_length=120, default="Company Growth Timeline")
    timeline_title = models.CharField(
        max_length=220,
        default="Built around practical distribution milestones.",
    )
    location_eyebrow = models.CharField(max_length=120, default="Our Location")
    location_title = models.CharField(max_length=220, default="Visit Us in Muttrah")
    location_description = models.TextField(
        default="Our headquarters and main distribution center are strategically located to serve the healthcare community efficiently."
    )
    location_map_url = models.URLField(
        max_length=500,
        blank=True,
        default="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3655.70020525746!2d58.542142999999996!3d23.615082400000002!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x3e91f900164bdb5b%3A0x1c2403fc0d8bf5e1!2sMUTTRAH%20PHARMACY!5e1!3m2!1sen!2sin!4v1781096686549!5m2!1sen!2sin"
    )

    class Meta:
        verbose_name = "About Page Content"
        verbose_name_plural = "About Page Content"

    def __str__(self):
        return "About Page Content"


class AboutHeroImage(models.Model):
    about_page = models.ForeignKey(
        AboutPage,
        on_delete=models.CASCADE,
        related_name="hero_images",
    )
    image = models.ImageField(upload_to="about_hero/")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return f"Hero Image {self.id}"


class AboutTimelineItem(models.Model):
    about_page = models.ForeignKey(
        AboutPage,
        on_delete=models.CASCADE,
        related_name="timeline_items",
    )
    title = models.CharField(max_length=160)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class ContactPage(SingletonPageModel):
    eyebrow = models.CharField(max_length=120, default="Contact Us")
    title = models.CharField(max_length=220, default="Send a product or distribution inquiry")
    description = models.TextField(
        default="Use the form below to post directly to the Django contact API."
    )
    address_label = models.CharField(max_length=80, default="Address")
    address = models.CharField(max_length=240, default="Muttrah, Muscat, Sultanate of Oman")
    email_label = models.CharField(max_length=80, default="Email")
    email = models.EmailField(default="info@muttrahpharmacy.com")
    phone_label = models.CharField(max_length=80, default="Phone")
    phone = models.CharField(max_length=80, default="+968 0000 0000")
    map_title = models.CharField(max_length=160, default="Muttrah, Muscat")
    map_description = models.TextField(
        default="Map embed placeholder ready for your Google Maps iframe."
    )
    google_maps_embed_url = models.URLField(blank=True)
    form_button_label = models.CharField(max_length=80, default="Submit Inquiry")
    inquiry_recipient_email = models.EmailField(
        default="jansabithjans@gmail.com",
        help_text="Email address where contact form submissions will be sent.",
    )

    class Meta:
        verbose_name = "Contact Page Content"
        verbose_name_plural = "Contact Page Content"

    def __str__(self):
        return "Contact Page Content"


class FooterContent(SingletonPageModel):
    brand_title = models.CharField(max_length=160, default="Muttrah Pharmacy")
    brand_description = models.TextField(
        default=(
            "Supplying pharmacies, clinics, hospitals, and orthopedic care teams "
            "across Oman with dependable warehouse-backed product availability."
        )
    )
    quick_links_title = models.CharField(max_length=120, default="Quick Links")
    contact_title = models.CharField(max_length=120, default="Contact Information")
    address = models.CharField(max_length=240, default="Muttrah, Muscat, Sultanate of Oman")
    email = models.EmailField(default="info@muttrahpharmacy.com")
    phone = models.CharField(max_length=80, default="+968 0000 0000")
    telephone = models.CharField(max_length=80, blank=True, default="+968 0000 0000")
    copyright_text = models.CharField(
        max_length=180,
        default="Copyright 2026 Muttrah Pharmacy. All rights reserved.",
    )
    bottom_note = models.CharField(max_length=160, default="Live Django REST catalog data.")

    class Meta:
        verbose_name = "Footer Content"
        verbose_name_plural = "Footer Content"

    def __str__(self):
        return "Footer Content"


class FooterQuickLink(models.Model):
    footer = models.ForeignKey(
        FooterContent,
        on_delete=models.CASCADE,
        related_name="quick_links",
    )
    label = models.CharField(max_length=80)
    url = models.CharField(max_length=240)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.label


class FooterSocialLink(models.Model):
    footer = models.ForeignKey(
        FooterContent,
        on_delete=models.CASCADE,
        related_name="social_links",
    )
    label = models.CharField(max_length=40)
    url = models.CharField(max_length=240, default="#top")
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.label


class ContactSubmission(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=80)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} - {self.email}"
