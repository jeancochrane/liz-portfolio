from io import BytesIO

from PIL import Image
import magic

from django.core.files.uploadedfile import InMemoryUploadedFile


class NoThumbnailException(Exception):
    """
    Blank exception used to handle the specific case where the
    admin uploads an image that is not a jpg or png.
    """
    pass


def make_thumbnail(buf):
    """
    Creates a thumbnail from an image.

    Params:
        `buf` – the original image as a streaming Django file object
    Returns:
        `thumb_file` - the thumbnail as a streaming Django file object
    """
    if buf.size < 200000:
        raise NoThumbnailException

    try:
        fname, ftype = buf.name.split('.')[0], buf.name.split('.')[1]
    except IndexError:  # in case the file doesn't have an extension
        fname = buf.name
        ftype = ''

    true_type = magic.from_buffer(buf.file.read(), mime=True)
    buf.file.seek(0)

    # Handle different filetypes
    if true_type == 'image/jpeg':
        format = 'JPEG'
    elif true_type == 'image/png':
        format = 'PNG'
    else:  # Anything else, just skip the thumbnail step
        raise NoThumbnailException

    # Configure PIL objects
    orig = Image.open(buf)
    img = orig.copy()

    # Max thumbnail size
    size = (1200, 1200)

    # Create thumbnail
    img.thumbnail(size, resample=4)

    # Generate file-like object from thumbnail
    img_file = BytesIO()
    img.save(img_file, format=format)
    thumb_file = InMemoryUploadedFile(file=img_file,
                                      field_name=None,
                                      name=fname + '_thumbnail.' + ftype,
                                      content_type=true_type,
                                      size=len(img_file.getvalue()),
                                      charset=None)

    return thumb_file
