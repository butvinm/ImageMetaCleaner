"""Conftest for tests.

Contains shared fixtures for tests.
"""


# Number of images in the `assets` directory.
from pathlib import Path
from typing import Generator

import pytest

from image_meta_cleaner.files_index import create_index_file, hash_file_data

TOTAL_IMAGES_COUNT = 4


@pytest.fixture
def assets_dir() -> Path:
    """Return path to the `assets` directory.

    Returns:
        Path: Path to the `assets` directory.
    """
    return Path('tests/assets')


@pytest.fixture
def assets_dir_with_index(assets_dir: Path) -> Generator[Path, None, None]:
    """Return path to the `assets` directory with index file.

    Index file is located in the same directory as the source
    with the name '.imc'.

    Args:
        assets_dir (Path): Path to the `assets` directory.

    Yields:
        Path: Path to the `assets` directory with index file.
    """
    image_path = assets_dir / '2.jpg'
    image_data = image_path.read_bytes()
    index = {
        assets_dir / '1.jpg': 'None',
        image_path: hash_file_data(image_data),
    }
    index_file_path = assets_dir / '.imc'
    index_file_path.write_text(create_index_file(index))

    yield assets_dir
    index_file_path.unlink()
