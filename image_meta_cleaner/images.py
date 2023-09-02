"""Images module.

Provide tools for reading images and processing their metadata.
"""


from io import BytesIO
from pathlib import Path

from PIL.Image import open as open_image


def is_image(file_path: Path) -> bool:
    """Check that file is an image.

    Supported formats: TIFF, JPEG, PNG, Webp, HEIC
    (actually, all formats supported by exifread)

    Args:
        file_path: Path to the file.

    Returns:
        bool: True if file of image type, False otherwise.
    """
    extensions = {'.tiff', '.jpeg', '.jpg', '.png', '.webp', '.heic'}
    return file_path.suffix.lower() in extensions


def get_image_without_meta(image_data: bytes) -> bytes:
    """Remove metadata from image.

    Args:
        image_data (bytes): Image data.

    Returns:
        bytes: Image data without metadata.
    """
    image = open_image(BytesIO(image_data))
    image.info.clear()
    image.getexif().clear()

    image_stream = BytesIO()
    image.save(image_stream, image.format)
    return image_stream.getvalue()
