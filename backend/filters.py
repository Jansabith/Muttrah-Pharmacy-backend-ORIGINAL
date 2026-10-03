from django.db.models import Q


def by_slug_or_id(field, value):
    """Filter on a related object by its web-address name (?company=tynor) or,
    so old links keep working, by its number (?company=7)."""
    value = value.strip()
    if value.isdigit():
        return Q(**{f'{field}_id': value})
    return Q(**{f'{field}__slug': value})
