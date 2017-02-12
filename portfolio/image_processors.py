from io import BytesIO

from PIL import Image
import magic

from django.core.files.uploadedfile import InMemoryUploadedFile

# Set possible image sizes
THUMBNAIL = (1200, 1200)  # For the grid layout
SMALL = (700, 1000)  # For small screens
MEDIUM = (1500, 2000)  # For medium screens
LARGE = (2000, 3000)


class NoThumbnailException(Exception):
    """
    Blank exception used to handle the specific case where the
    admin uploads an image that is not a jpg or png.
    """
    pass


def resize(buf, img_size='thumbnail'):
    """
    Creates a thumbnail from an image.

    Params:
        `buf` – the original image as a streaming Django file object
    Returns:
        `thumb_file` - the thumbnail as a streaming Django file object
    """
    if img_size == 'thumbnail':
        max_size = THUMBNAIL
    elif img_size == 'small':
        max_size = SMALL
    elif img_size == 'medium':
        max_size = MEDIUM
    elif img_size == 'large':
        max_size = LARGE
    else:
        raise Exception("""
            '%s' is not a valid image size. Accepted sizes:
             thumbnail, small, medium.""" % img_size)

    if buf.size < 200000:
        raise NoThumbnailException

    try:
        fname, ftype = buf.name.split('.')[0], buf.name.split('.')[1]
        outname = fname + '_' + img_size + '.' + ftype
    except IndexError:  # in case the file doesn't have an extension
        fname = buf.name
        outname = fname + '_' + img_size

    true_type = magic.from_buffer(buf.file.read(), mime=True)
    buf.file.seek(0)

    # Handle different filetypes
    if true_type == 'image/jpeg':
        format = 'JPEG'
    elif true_type == 'image/png':
        format = 'PNG'
    else:  # Anything else, just skip the thumbnail step
        raise Exception("""
            '%s' is not a valid image type for formatting. Accepted types:
             jpeg, png.""" % true_type)

    # Configure PIL objects
    orig = Image.open(buf)
    img = orig.copy()

    # Create thumbnail
    img.thumbnail(max_size, resample=4)

    # Generate file-like object from thumbnail
    img_file = BytesIO()
    img.save(img_file, format=format)
    thumb_file = InMemoryUploadedFile(file=img_file,
                                      field_name=None,
                                      name=outname,
                                      content_type=true_type,
                                      size=len(img_file.getvalue()),
                                      charset=None)
    img_file.seek(0)
    buf.file.seek(0)

    return thumb_file
