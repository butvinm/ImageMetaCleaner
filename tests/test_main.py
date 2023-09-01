"""Test main module."""

from pathlib import Path

from image_meta_cleaner.main import Ok, process_dir
from tests.conftest import TOTAL_IMAGES_COUNT


def test_process(assets_dir: Path) -> None:
    """Test process_dir function.

    Function called in `pure` mode should not save files.

    Args:
        assets_dir (Path): Path to assets directory.
    """
    processing_results = process_dir(assets_dir, pure=True)
    assert len(processing_results) == TOTAL_IMAGES_COUNT
    for processing_result in processing_results:
        assert isinstance(processing_result, Ok)


def test_index(assets_dir_with_index: Path) -> None:
    """Test process_dir function with index file.

    In test index file 1.jpg stored with old hash and
    2.jpg stored with new hash.

    So, we expect that 1.jpg will be processed and 2.jpg will not.

    Args:
        assets_dir_with_index (Path): Path to assets directory with index file.
    """
    processing_results = process_dir(assets_dir_with_index, pure=True)
    assert len(processing_results) == TOTAL_IMAGES_COUNT - 1
