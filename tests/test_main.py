"""Test main module."""

from pathlib import Path

from image_meta_cleaner.main import process_dir
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
        assert processing_result.ok
