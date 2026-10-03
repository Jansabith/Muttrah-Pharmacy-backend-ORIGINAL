from django.db import migrations, models

SLUG_HELP = (
    'Name used in the website address, e.g. /products?company=tynor. '
    'Filled in automatically from the name; changing it later breaks old links.'
)


class Migration(migrations.Migration):
    """Every row got a slug in 0005, so the columns can now be required and unique."""

    dependencies = [
        ('companies', '0005_fill_company_and_line_slugs'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='slug',
            field=models.SlugField(blank=True, help_text=SLUG_HELP, max_length=120, unique=True),
        ),
        migrations.AlterField(
            model_name='companyline',
            name='slug',
            field=models.SlugField(blank=True, help_text=SLUG_HELP, max_length=120),
        ),
        migrations.AddConstraint(
            model_name='companyline',
            constraint=models.UniqueConstraint(fields=('company', 'slug'), name='unique_company_line_slug'),
        ),
    ]
