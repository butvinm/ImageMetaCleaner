"""Conftest for tests.

Contains shared fixtures for tests.
"""


from pathlib import Path

import pytest

# Number of images in the `assets` directory.
TOTAL_IMAGES_COUNT = 4


@pytest.fixture
def assets_dir() -> Path:
    """Return path to the `assets` directory.

    Returns:
        Path: Path to the `assets` directory.
    """
    return Path('tests/assets')
