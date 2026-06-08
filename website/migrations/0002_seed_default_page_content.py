from django.db import migrations


def seed_default_content(apps, schema_editor):
    HomePage = apps.get_model("website", "HomePage")
    HomeFeature = apps.get_model("website", "HomeFeature")
    AboutPage = apps.get_model("website", "AboutPage")
    AboutTimelineItem = apps.get_model("website", "AboutTimelineItem")
    ContactPage = apps.get_model("website", "ContactPage")

    home_page = HomePage.objects.first() or HomePage.objects.create()
    if not HomeFeature.objects.filter(home_page=home_page).exists():
        default_features = [
            (
                "Django-admin managed live catalog",
                "A practical operating model for procurement teams that need clear catalog access and fast communication.",
            ),
            (
                "Pharmaceutical and orthopedic focus",
                "Medical product presentation shaped around pharmacy, clinic, and orthopedic supply workflows.",
            ),
            (
                "Warehouse-first stock visibility",
                "Content and products stay aligned with your backend catalog and administration process.",
            ),
            (
                "Oman-wide distribution support",
                "A professional digital catalog for healthcare buyers across the Sultanate of Oman.",
            ),
        ]
        HomeFeature.objects.bulk_create(
            [
                HomeFeature(
                    home_page=home_page,
                    title=title,
                    description=description,
                    order=index,
                )
                for index, (title, description) in enumerate(default_features, start=1)
            ]
        )

    about_page = AboutPage.objects.first() or AboutPage.objects.create()
    if not AboutTimelineItem.objects.filter(about_page=about_page).exists():
        default_timeline = [
            ("Foundation", "Established as a trusted pharmacy distribution partner."),
            ("Expansion", "Broadened coverage into orthopedic and medical supply lines."),
            ("Digital Catalog", "Connected product discovery to Django REST APIs."),
            ("Next Phase", "Faster inquiry handling for healthcare buyers across Oman."),
        ]
        AboutTimelineItem.objects.bulk_create(
            [
                AboutTimelineItem(
                    about_page=about_page,
                    title=title,
                    description=description,
                    order=index,
                )
                for index, (title, description) in enumerate(default_timeline, start=1)
            ]
        )

    ContactPage.objects.first() or ContactPage.objects.create()


def reverse_seed_default_content(apps, schema_editor):
    HomeFeature = apps.get_model("website", "HomeFeature")
    AboutTimelineItem = apps.get_model("website", "AboutTimelineItem")
    HomeFeature.objects.all().delete()
    AboutTimelineItem.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_default_content, reverse_seed_default_content),
    ]
