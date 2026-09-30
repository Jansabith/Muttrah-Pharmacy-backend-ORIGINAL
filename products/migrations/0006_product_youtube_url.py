from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_alter_product_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='youtube_url',
            field=models.URLField(blank=True, help_text='Optional YouTube video link, for example: https://www.youtube.com/watch?v=XXXXXXXXXXX'),
        ),
    ]
