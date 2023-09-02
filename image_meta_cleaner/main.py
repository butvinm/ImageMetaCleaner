"""Entry point of the script."""


import json
import sys
from pathlib import Path
from time import sleep

from image_meta_cleaner.files_index import FilesIndex
from image_meta_cleaner.images import is_image
from image_meta_cleaner.location import Location
from image_meta_cleaner.processing import (
    Err,
    Ok,
    ProcessingResult,
    process_images,
)


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
        return FilesIndex()

    index_file_data = index_file_path.read_text()
    return FilesIndex.from_index_file(index_file_data)


def save_files_index(source: Path, index: FilesIndex) -> None:
    """Save processed files to index file.

    Index file is located in the same directory as the source
    with the name '.imc'.

    Args:
        source (Path): Path to the source directory.
        index (FilesIndex): Processed files index.
    """
    index_file_path = source / '.imc'
    index_file_data = index.build_index_file()
    index_file_path.write_text(index_file_data)


def save_location(image_path: Path, location: Location) -> Path:
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


def get_dir_images(source: Path) -> list[tuple[Path, bytes]]:
    """Iterate over images files in directory.

    Args:
        source (Path): Directory path.

    Returns:
        list[tuple[Path, bytes]]: Images pathes and contents
    """
    images: list[tuple[Path, bytes]] = []
    for file_path in source.glob('**/*'):
        if file_path.is_file() and is_image(file_path):
            images.append((
                file_path,
                file_path.read_bytes(),
            ))

    return images


def print_result(results: list[ProcessingResult]) -> None:
    """Print processing result info.

    Args:
        results (list[ProcessingResult]): Results of images processing.
    """
    success_results: list[Ok] = []
    failure_results: list[Err] = []
    for result in results:
        if isinstance(result, Ok):
            success_results.append(result)
        else:
            failure_results.append(result)

    print('Processed: {total}\tSuccess: {success}\tFailure: {failure}'.format(
        total=len(results),
        success=len(success_results),
        failure=len(failure_results),
    ))
    for failure in failure_results:
        print('Fail to process {file_path}: {message}'.format(
            file_path=failure.file_path,
            message=failure.message,
        ))
        if failure.error is not None:
            print(failure.error)


def process_dir(source: Path) -> None:
    """Process images in directory.

    Args:
        source (Path): Directory path.
    """
    index = get_files_index(source)
    images = get_dir_images(source)
    processing_results, new_index = process_images(images, index)
    for result in processing_results:
        if isinstance(result, Ok):
            if result.location is not None:
                save_location(result.file_path, result.location)

            result.file_path.write_bytes(result.file_data)

    save_files_index(source, new_index)
    print_result(processing_results)


def watch(source: Path, delay: int) -> None:
    """Continuously process files in directory.

    Args:
        source (Path): Directory path.
        delay (int): Delay between processing in seconds.
    """
    while source.exists():
        process_dir(source)
        sleep(delay)


if __name__ == '__main__':
    match sys.argv:
        case _, source:
            process_dir(Path(source))
        case _, source, delay if delay.isdecimal():
            watch(Path(source), int(delay))
        case _:
            print('Usage: imc source [delay]')
            exit(1)
