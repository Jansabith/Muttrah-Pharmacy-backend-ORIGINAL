# Generated for editable footer telephone number.

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("website", "0005_footer_content"),
    ]

    operations = [
        migrations.AddField(
            model_name="footercontent",
            name="telephone",
            field=models.CharField(blank=True, default="+968 0000 0000", max_length=80),
        ),
    ]
