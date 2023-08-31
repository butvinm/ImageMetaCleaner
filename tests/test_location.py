"""Tests for location module."""

import json
from pathlib import Path

from image_meta_cleaner.location import Location, get_file_gps_location


def get_location_from_json(path: Path) -> Location:
    """Get location from json file.

    Args:
        path (Path): Path to the json file.

    Returns:
        Location: Location object.
    """
    location_data = json.loads(path.read_text())
    return Location(
        latitude=location_data['latitude'],
        longitude=location_data['longitude'],
    )


def test_get_file_gps_location(assets_dir: Path) -> None:
    """Test get_file_gps_location function.

    Correct location of images stored in <image_name>.json files.

    Args:
        assets_dir (Path): Path to the `assets` directory.
    """
    # test file with correct metadata
    image_path = assets_dir / '1.jpg'
    image_data = image_path.read_bytes()
    location_path = assets_dir / '1.json'
    correct_location = get_location_from_json(location_path)
    assert get_file_gps_location(image_data) == correct_location

    # test file without gps in metadata
    image_path = assets_dir / '4.jpg'
    image_data = image_path.read_bytes()
    assert get_file_gps_location(image_data) is None
