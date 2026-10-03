from django.db import migrations
from django.utils.text import slugify


def unique_slug(name, taken, fallback):
    base = slugify(name)[:110].strip('-') or fallback
    slug = base
    counter = 2
    while slug in taken:
        slug = f'{base}-{counter}'
        counter += 1
    taken.add(slug)
    return slug


def fill_slugs(apps, schema_editor):
    """Gives every existing brand and product line a web address name taken
    from its name, e.g. "BELL SONS & CO. (UK)" -> "bell-sons-co-uk"."""
    Company = apps.get_model('companies', 'Company')
    CompanyLine = apps.get_model('companies', 'CompanyLine')

    taken = set()
    for company in Company.objects.order_by('id'):
        company.slug = unique_slug(company.name, taken, f'brand-{company.id}')
        company.save(update_fields=['slug'])

    # Product line names only need to be unique within their brand
    taken_per_company = {}
    for line in CompanyLine.objects.order_by('id'):
        taken_lines = taken_per_company.setdefault(line.company_id, set())
        line.slug = unique_slug(line.name, taken_lines, f'line-{line.id}')
        line.save(update_fields=['slug'])


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0004_company_and_line_slug'),
    ]

    operations = [
        migrations.RunPython(fill_slugs, migrations.RunPython.noop),
    ]
