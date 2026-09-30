import django.utils.timezone
from django.db import migrations, models

SEO_TITLE_HELP = (
    'Optional. Title shown in Google results and the browser tab (best under 60 characters). '
    '" | Muttrah Pharmacy" is added automatically. Leave empty to use the product name.'
)
SEO_DESCRIPTION_HELP = (
    'Optional. Text shown under the title in Google results (best 120-155 characters). '
    'Leave empty to use the start of the product description.'
)


def seo_fields():
    return (
        ('meta_title', models.CharField('SEO title', max_length=255, blank=True, null=True, help_text=SEO_TITLE_HELP)),
        ('meta_description', models.TextField('SEO description', blank=True, null=True, help_text=SEO_DESCRIPTION_HELP)),
    )


def add_missing_seo_columns(apps, schema_editor):
    # An earlier migration (deleted from the codebase) already created these
    # columns in some databases, so only add the ones that are missing.
    connection = schema_editor.connection
    Product = apps.get_model('products', 'Product')
    table = Product._meta.db_table
    with connection.cursor() as cursor:
        existing = {column.name for column in connection.introspection.get_table_description(cursor, table)}

    for name, field in seo_fields():
        if name not in existing:
            field.set_attributes_from_name(name)
            schema_editor.add_field(Product, field)


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0006_product_youtube_url'),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AddField(model_name='product', name=name, field=field)
                for name, field in seo_fields()
            ],
            database_operations=[
                migrations.RunPython(add_missing_seo_columns, migrations.RunPython.noop),
            ],
        ),
        # Existing products get the migration time as their first "updated" date
        migrations.AddField(
            model_name='product',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
