"""Entry point of the script."""


import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from image_meta_cleaner.images import get_image_without_meta, is_image
from image_meta_cleaner.location import Location, get_file_gps_location


@dataclass
class ProcessingResult(object):
    """Result of image processing."""

    ok: bool
    image_path: Path
    location_info_path: Optional[Path]
    file_hash: Optional[int]
    message: Optional[str]
    error: Optional[Exception]

    @classmethod
    def failure(
        cls,
        image_path: Path,
        message: str,
        error: Exception,
    ) -> 'ProcessingResult':
        """Create failure result.

        Args:
            image_path (Path): Path to the image.
            message (str): Message.
            error (Exception): Exception.

        Returns:
            ProcessingResult: Failure result.
        """
        return cls(
            ok=False,
            image_path=image_path,
            location_info_path=None,
            file_hash=None,
            message=message,
            error=error,
        )


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


def process_image(file_path: Path, pure: bool = False) -> ProcessingResult:
    """Process image file.

    Remove metadata from image and save location info of the file.

    Args:
        file_path (Path): Path to the image.
        pure (bool): If True, files will not be saved.

    Returns:
        ProcessingResult: Result of the processing.
    """
    try:
        file_data = file_path.read_bytes()
    except OSError as read_error:
        return ProcessingResult.failure(
            image_path=file_path,
            message='Cannot read file',
            error=read_error,
        )

    location = get_file_gps_location(file_data)
    if location is not None and not pure:
        location_info_path = save_location_info(location, file_path)
    else:
        location_info_path = None

    try:
        image_without_meta = get_image_without_meta(file_data)
    except Exception as get_meta_error:
        return ProcessingResult.failure(
            image_path=file_path,
            message='Cannot remove metadata',
            error=get_meta_error,
        )

    if not pure:
        image_without_meta.save(file_path)

    file_hash = hash(file_data)
    return ProcessingResult(
        ok=True,
        image_path=file_path,
        location_info_path=location_info_path,
        file_hash=file_hash,
        message='Success',
        error=None,
    )


def process_dir(source: Path, pure: bool = False) -> list[ProcessingResult]:
    """Process images in directory.

    Remove metadata from images and save location info of all
    files in provided directory and subdirectories.

    Args:
        source (Path): Path to the directory containing images.
        pure (bool): If True, files will not be saved.

    Returns:
        list[ProcessingResult]: List of processing results.
    """
    processing_results: list[ProcessingResult] = []
    for file_path in source.glob('**/*'):
        if file_path.is_dir() or not is_image(file_path):
            continue

        process_result = process_image(file_path, pure)
        processing_results.append(process_result)

    return processing_results


if __name__ == '__main__':
    args = sys.argv[1:]

    if len(args) != 1:
        print('Usage: image_meta_cleaner <source>')
        sys.exit(1)

    source = Path(args[0])

    processing_results = process_dir(source)
    success_results: list[ProcessingResult] = []
    failure_results: list[ProcessingResult] = []
    for processing_result in processing_results:
        if processing_result.ok:
            success_results.append(processing_result)
        else:
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
