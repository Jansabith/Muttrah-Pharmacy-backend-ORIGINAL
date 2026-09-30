import os
from io import BytesIO

from django.core.files.base import ContentFile
from PIL import Image, ImageOps


def convert_to_webp(field_file, quality=85):
    """Re-encode a newly uploaded image as WebP before it is stored.

    Only runs for fresh uploads (not yet committed to storage), so editing
    other fields of an existing record never re-processes its image.
    Files that are already WebP are kept as they are.
    """
    if not field_file or getattr(field_file, '_committed', True):
        return
    if field_file.name.lower().endswith('.webp'):
        return

    image = Image.open(field_file)
    # Keep the colour profile (e.g. Display P3 from phones/Photoshop) so colours
    # in the WebP match the uploaded file instead of looking washed out
    icc_profile = image.info.get('icc_profile')
    # Phone photos store rotation in EXIF; apply it so images aren't sideways
    image = ImageOps.exif_transpose(image)

    has_alpha = image.mode in ('RGBA', 'LA') or (
        image.mode == 'P' and 'transparency' in image.info
    )
    image = image.convert('RGBA' if has_alpha else 'RGB')

    buffer = BytesIO()
    save_options = {'format': 'WEBP', 'quality': quality, 'method': 6}
    if icc_profile:
        save_options['icc_profile'] = icc_profile
    image.save(buffer, **save_options)

    base_name = os.path.splitext(os.path.basename(field_file.name))[0]
    field_file.save(f'{base_name}.webp', ContentFile(buffer.getvalue()), save=False)
