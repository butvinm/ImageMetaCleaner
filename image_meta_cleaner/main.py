"""Entry point of the script."""


import logging
import sys
from pathlib import Path
from time import sleep

from image_meta_cleaner.files_index import FilesIndex
from image_meta_cleaner.images import is_image
from image_meta_cleaner.processing import (
    Err,
    Ok,
    ProcessingResult,
    process_images,
)

logging.basicConfig(
    format='%(asctime)s %(levelname)s %(message)s',  # noqa:WPS323
    level=logging.INFO,
    filename='imc.log',
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


def get_image_location_info(result: ProcessingResult) -> str:
    """Build string with image location info.

    String format: `file_path latitude longitude`

    Args:
        result (ProcessingResult): \
            Result of image processing with pathes and location info.

    Returns:
        str: String with image location info.
    """
    info_template = '{file_path:<80}\t{latitude:<9.6f}\t{longitude:<9.6f}'
    if isinstance(result, Ok) and result.location is not None:
        return info_template.format(
            file_path=str(result.file_path),
            latitude=result.location.latitude,
            longitude=result.location.longitude,
        )

    return info_template.format(
        file_path=str(result.file_path),
        latitude=0,
        longitude=0,
    )


def save_locations(
    source: Path,
    results: list[ProcessingResult],
) -> Path:
    """Save locations info.

    Locations stored in `location.txt` file

    Args:
        source (Path): Root directory path.
        results (list[ProcessingResult]): \
            Results of images processing with pathes and location info.

    Returns:
        Path: Path to the saved location info.
    """
    locations_info = '\n'.join(
        get_image_location_info(result)
        for result in results
    )
    locations_path = source / 'locations.txt'
    locations_path.write_text(locations_info)
    return locations_path


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


def log_result(results: list[ProcessingResult]) -> None:
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

    logging.info('Processed: {total}\tSuccess: {success}\tFailure: {failure}'.format(  # noqa: E501
        total=len(results),
        success=len(success_results),
        failure=len(failure_results),
    ))
    for failure in failure_results:
        logging.warning('Fail to process {file_path}: {message}'.format(
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
            result.file_path.write_bytes(result.file_data)

    save_locations(source, processing_results)
    save_files_index(source, new_index)
    log_result(processing_results)


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
            input('Press any key to exit...')
        case _, source, delay if delay.isdecimal():
            watch(Path(source), int(delay))
            input('Press any key to exit...')
        case _:
            logging.error('Usage: imc source [delay]')
            sys.exit(1)

    print('See logs at imc.log')
