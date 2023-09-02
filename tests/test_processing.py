"""Tests for images processing module."""

from pathlib import Path

from image_meta_cleaner.files_index import FilesIndex, hash_file_data
from image_meta_cleaner.images import is_image
from image_meta_cleaner.processing import Ok, process_image, process_images
from tests.conftest import TOTAL_IMAGES_COUNT


def test_process_image(assets_dir: Path) -> None:
    """Test process_image function.

    Args:
        assets_dir (Path): Assets directory path.
    """
    # Image with location info
    image_path = assets_dir / '1.jpg'
    image_result = process_image(image_path, image_path.read_bytes())
    assert isinstance(image_result, Ok)
    assert image_result.location is not None

    # Image without location info
    image_path = assets_dir / '4.jpg'
    image_result = process_image(image_path, image_path.read_bytes())
    assert isinstance(image_result, Ok)
    assert image_result.location is None


def test_process_images(assets_dir: Path) -> None:
    """Test process_images function.

    Args:
        assets_dir (Path): Assets directory path.
    """
    images = [
        (file_path, file_path.read_bytes())
        for file_path in assets_dir.glob('**/*')
        if is_image(file_path)
    ]
    # With clear index
    # Expect all files processed
    processing_results, new_index = process_images(images, FilesIndex())
    assert len(processing_results) == TOTAL_IMAGES_COUNT
    assert len(new_index) == TOTAL_IMAGES_COUNT
    for image_result in processing_results:
        assert isinstance(image_result, Ok)

    # With old `1.jpg`` in index and up-to-date `2.jpg` in index
    # Expect update of `1.jpg` in index and skipping `2.jpg`
    index = FilesIndex({
        images[0][0]: 'None',
        images[1][0]: hash_file_data(images[1][1]),
    })
    processing_results, new_index = process_images(images, index)
    assert len(processing_results) == TOTAL_IMAGES_COUNT - 1
    assert len(new_index) == TOTAL_IMAGES_COUNT
    assert index[images[0][0]] != new_index[images[0][0]]
    assert index[images[1][0]] == new_index[images[1][0]]
