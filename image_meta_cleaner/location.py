"""Location module.

Provides tools for working with image location data.
"""

from dataclasses import dataclass
from io import BytesIO
from typing import Optional

from exifread import process_file
from exifread.utils import get_gps_coords


@dataclass
class Location(object):
    """Location data of an image."""

    latitude: float
    longitude: float

    def __eq__(self, other: object) -> bool:
        """Compare two Location objects.

        Latitude and longitude are compared with a threshold of 0.00001.

        Args:
            other (object): Object to compare with.

        Returns:
            bool: True if objects are equal, False otherwise.
        """
        if not isinstance(other, Location):
            return False

        equality_threshold = 0.00001
        return (
            abs(self.latitude - other.latitude) < equality_threshold
            and abs(self.longitude - other.longitude) < equality_threshold
        )


def get_file_gps_location(file_data: bytes) -> Optional[Location]:
    """Read location data from file.

    Args:
        file_data (bytes): File data.

    Returns:
        Optional[Location]: Location data.
    """
    tags = process_file(BytesIO(file_data))
    coords: tuple[int, int] | tuple[()] = get_gps_coords(tags)  # type: ignore
    if not coords:
        return None

    latitude, longitude = coords
    return Location(latitude, longitude)
