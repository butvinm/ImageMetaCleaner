"""Images processing module.

Contains processing pipelines that compose index reading, location extracting
and removing of metadata.
"""


from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from image_meta_cleaner.files_index import FilesIndex, hash_file_data
from image_meta_cleaner.images import get_image_without_meta
from image_meta_cleaner.location import Location, get_file_gps_location


@dataclass
class Ok(object):
    """Success result of image processing."""

    file_path: Path
    file_data: bytes
    location: Optional[Location]
    file_hash: str


@dataclass
class Err(object):
    """Failure result of image processing."""

    file_path: Path
    message: str
    error: Optional[Exception]


# Result of image processing.
ProcessingResult = Ok | Err


def process_image(file_path: Path, file_data: bytes) -> ProcessingResult:
    """Process image file.

    Extract location info and remove metadata.

    Args:
        file_path (Path): File path.
        file_data (bytes): File content.

    Returns:
        ProcessingResult: Result with processing info.
    """
    location = get_file_gps_location(file_data)

    try:
        no_meta_file_data = get_image_without_meta(file_data)
    except Exception as metadata_error:
        return Err(
            file_path=file_path,
            message='Cannot remove metadata',
            error=metadata_error,
        )

    no_meta_file_hash = hash_file_data(no_meta_file_data)
    return Ok(
        file_path=file_path,
        file_data=no_meta_file_data,
        location=location,
        file_hash=no_meta_file_hash,
    )


def process_images(
    images: list[tuple[Path, bytes]],
    index: FilesIndex,
) -> tuple[list[ProcessingResult], FilesIndex]:
    """Process images in directory.

    Remove metadata from images and save location info of all
    files in provided directory and subdirectories.

    Args:
        images (list[tuple[Path, bytes]]): Images to process.
        index (FilesIndex): Index with processed files.

    Returns:
        list[ProcessingResult]: Processing results.
        FilesIndex: Update files index.
    """
    processing_results: list[ProcessingResult] = []
    new_index = FilesIndex()
    for file_path, file_data in images:
        if index.verify_file(file_path, file_data):
            file_hash = index.get(file_path)
            if file_hash is not None:
                new_index[file_path] = file_hash
        else:
            file_result = process_image(file_path, file_data)
            processing_results.append(file_result)
            if isinstance(file_result, Ok):
                new_index[file_path] = file_result.file_hash

    return processing_results, new_index
