"""Entry point of the script."""


import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from image_meta_cleaner.files_index import (
    FilesIndex,
    create_index_file,
    hash_file_data,
    parse_index_file,
)
from image_meta_cleaner.images import get_image_without_meta, is_image
from image_meta_cleaner.location import Location, get_file_gps_location


@dataclass
class Ok(object):
    """Success result of image processing."""

    image_path: Path
    location_info_path: Optional[Path]
    file_hash: str
    updated: bool


@dataclass
class Failure(object):
    """Failure result of image processing."""

    image_path: Path
    message: str
    error: Exception


# Result of image processing.
Result = Ok | Failure


def get_files_index(source: Path) -> FilesIndex:
    """Get processed files from index file.

    Index file is located in the same directory as the source
    with the name '.imc'.

    Args:
        source (Path): Path to the source directory.

    Returns:
        FilesIndex: Processed files index.
    """
    index_file_path = source / '.imc'
    if not index_file_path.exists():
        return {}

    index_file_data = index_file_path.read_text()
    return parse_index_file(index_file_data)


def save_files_index(source: Path, index: FilesIndex) -> None:
    """Save processed files to index file.

    Index file is located in the same directory as the source
    with the name '.imc'.

    Args:
        source (Path): Path to the source directory.
        index (FilesIndex): Processed files index.
    """
    index_file_path = source / '.imc'
    index_file_data = create_index_file(index)
    index_file_path.write_text(index_file_data)


def save_location_info(location: Location, image_path: Path) -> Path:
    """Save location info of the image.

    Location will be saved in the same directory as the image
    with the same name and extension '.json'.

    Args:
        location (Location): Location data.
        image_path (Path): Path to the image.

    Returns:
        Path: Path to the saved location info.
    """
    location_file_path = image_path.with_suffix('.json')
    location_data = {
        'latitude': location.latitude,
        'longitude': location.longitude,
    }
    json.dump(location_data, location_file_path.open('w'))
    return location_file_path


def process_image(
    file_path: Path,
    index: FilesIndex,
    pure: bool = False,
) -> Result:
    """Process image file.

    Remove metadata from image and save location info of the file.

    Args:
        file_path (Path): Path to the image.
        index (FilesIndex): Processed files index.
        pure (bool): If True, files will not be saved.

    Returns:
        Result: Processing result.
    """
    try:
        file_data = file_path.read_bytes()
    except OSError as read_error:
        return Failure(
            image_path=file_path,
            message='Cannot read file',
            error=read_error,
        )

    file_hash = hash_file_data(file_data)
    if file_path in index and index[file_path] == file_hash:
        return Ok(
            image_path=file_path,
            location_info_path=None,
            file_hash=file_hash,
            updated=False,
        )

    location = get_file_gps_location(file_data)
    if location is not None and not pure:
        location_info_path = save_location_info(location, file_path)
    else:
        location_info_path = None

    try:
        image_without_meta = get_image_without_meta(file_data)
    except Exception as get_meta_error:
        return Failure(
            image_path=file_path,
            message='Cannot remove metadata',
            error=get_meta_error,
        )

    if not pure:
        image_without_meta.save(file_path)

    return Ok(
        image_path=file_path,
        location_info_path=location_info_path,
        file_hash=file_hash,
        updated=True,
    )


def process_dir(source: Path, pure: bool = False) -> list[Result]:
    """Process images in directory.

    Remove metadata from images and save location info of all
    files in provided directory and subdirectories.

    Args:
        source (Path): Path to the directory containing images.
        pure (bool): If True, files will not be saved.

    Returns:
        list[ProcessingResult]: List of processing results.
    """
    index = get_files_index(source)
    processing_results: list[Result] = []
    for file_path in source.glob('**/*'):
        file_path = file_path.absolute()
        if file_path.is_dir() or not is_image(file_path):
            continue

        image_result = process_image(file_path, index, pure)
        match image_result:
            case Ok(image_path, _, file_hash, True):
                processing_results.append(image_result)
                index[image_path.absolute()] = file_hash
            case Failure(image_path, _, _):
                processing_results.append(image_result)

    if not pure:
        save_files_index(source, index)

    return processing_results


if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) != 1:
        print('Usage: image_meta_cleaner <source>')
        sys.exit(1)

    source = Path(args[0])

    processing_results = process_dir(source)
    success_results: list[Ok] = []
    failure_results: list[Failure] = []
    for processing_result in processing_results:
        match processing_result:
            case Ok():
                success_results.append(processing_result)
            case Failure():
                failure_results.append(processing_result)

    print('Files: {files} Success: {success} Failure: {failure}'.format(
        files=len(processing_results),
        success=len(success_results),
        failure=len(failure_results),
    ))
    for failure_result in failure_results:
        print('Failure: {path} - {message}'.format(
            path=failure_result.image_path,
            message=failure_result.message,
        ))
        if failure_result.error is not None:
            print('Error: {error}'.format(
                error=failure_result.error,
            ))
