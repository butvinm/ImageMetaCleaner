"""Tests for images module."""

from io import BytesIO
from pathlib import Path

from PIL.Image import open as open_image

from image_meta_cleaner.images import get_image_without_meta, is_image


def test_is_image(assets_dir: Path) -> None:
    """Test is_image function.

    Args:
        assets_dir (Path): Path to assets directory.
    """
    # image file
    assert is_image(assets_dir / '1.jpg')

    # non-image file
    assert not is_image(assets_dir / '1.json')


def test_get_image_without_meta(assets_dir: Path) -> None:
    """Test get_image_without_meta function.

    Args:
        assets_dir (Path): Path to assets directory.
    """
    image_path = assets_dir / '1.jpg'
    image_data = image_path.read_bytes()
    no_meta_image_data = get_image_without_meta(image_data)

    image = open_image(BytesIO(no_meta_image_data))
    assert not len(image.getexif())
