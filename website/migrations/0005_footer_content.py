# Generated for editable footer content.

import django.db.models.deletion
from django.db import migrations, models


def seed_footer_content(apps, schema_editor):
    FooterContent = apps.get_model("website", "FooterContent")
    FooterQuickLink = apps.get_model("website", "FooterQuickLink")
    FooterSocialLink = apps.get_model("website", "FooterSocialLink")

    footer, _ = FooterContent.objects.get_or_create(
        defaults={
            "brand_title": "Muttrah Pharmacy",
            "brand_description": (
                "Supplying pharmacies, clinics, hospitals, and orthopedic care teams "
                "across Oman with dependable warehouse-backed product availability."
            ),
            "quick_links_title": "Quick Links",
            "contact_title": "Contact Information",
            "address": "Muttrah, Muscat, Sultanate of Oman",
            "email": "info@muttrahpharmacy.com",
            "phone": "+968 0000 0000",
            "copyright_text": "Copyright 2026 Muttrah Pharmacy. All rights reserved.",
            "bottom_note": "Live Django REST catalog data.",
        }
    )

    quick_links = [
        ("Home", "/", 0),
        ("Products", "/products", 1),
        ("About Us", "/about", 2),
        ("Contact Us", "/contact", 3),
    ]
    for label, url, order in quick_links:
        FooterQuickLink.objects.get_or_create(
            footer=footer,
            label=label,
            defaults={"url": url, "order": order, "is_active": True},
        )

    social_links = [
        ("in", "#top", 0),
        ("x", "#top", 1),
        ("f", "#top", 2),
    ]
    for label, url, order in social_links:
        FooterSocialLink.objects.get_or_create(
            footer=footer,
            label=label,
            defaults={"url": url, "order": order, "is_active": True},
        )


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0004_homepage_trust_eyebrow_homepage_trust_title_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="FooterContent",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("brand_title", models.CharField(default="Muttrah Pharmacy", max_length=160)),
                (
                    "brand_description",
                    models.TextField(
                        default=(
                            "Supplying pharmacies, clinics, hospitals, and orthopedic care teams "
                            "across Oman with dependable warehouse-backed product availability."
                        )
                    ),
                ),
                ("quick_links_title", models.CharField(default="Quick Links", max_length=120)),
                (
                    "contact_title",
                    models.CharField(default="Contact Information", max_length=120),
                ),
                (
                    "address",
                    models.CharField(
                        default="Muttrah, Muscat, Sultanate of Oman",
                        max_length=240,
                    ),
                ),
                ("email", models.EmailField(default="info@muttrahpharmacy.com", max_length=254)),
                ("phone", models.CharField(default="+968 0000 0000", max_length=80)),
                (
                    "copyright_text",
                    models.CharField(
                        default="Copyright 2026 Muttrah Pharmacy. All rights reserved.",
                        max_length=180,
                    ),
                ),
                (
                    "bottom_note",
                    models.CharField(
                        default="Live Django REST catalog data.",
                        max_length=160,
                    ),
                ),
            ],
            options={
                "verbose_name": "Footer Content",
                "verbose_name_plural": "Footer Content",
            },
        ),
        migrations.CreateModel(
            name="FooterQuickLink",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("label", models.CharField(max_length=80)),
                ("url", models.CharField(max_length=240)),
                ("order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "footer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="quick_links",
                        to="website.footercontent",
                    ),
                ),
            ],
            options={
                "ordering": ["order", "id"],
            },
        ),
        migrations.CreateModel(
            name="FooterSocialLink",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("label", models.CharField(max_length=40)),
                ("url", models.CharField(default="#top", max_length=240)),
                ("order", models.PositiveIntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                (
                    "footer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="social_links",
                        to="website.footercontent",
                    ),
                ),
            ],
            options={
                "ordering": ["order", "id"],
            },
        ),
        migrations.RunPython(seed_footer_content, migrations.RunPython.noop),
    ]
