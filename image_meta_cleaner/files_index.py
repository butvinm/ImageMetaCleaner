"""Files index module.

This module contains functions for creating and reading files index
with information about processed files.
"""


import hashlib
from pathlib import Path

# Files index is a dict with file pathes and content hashes.
FilesIndex = dict[Path, str]


def parse_index_file(file_data: str) -> FilesIndex:
    """Parse index file.

    Args:
        file_data (str): Index file data.

    Returns:
        FilesIndex: Index.
    """
    index: FilesIndex = {}
    for line in file_data.splitlines():
        if not line:
            continue

        file_path, file_hash = line.split('\t')
        index[Path(file_path)] = file_hash

    return index


def create_index_file(index: FilesIndex) -> str:
    """Create index file.

    Args:
        index (FilesIndex): Index.

    Returns:
        str: Index file data.
    """
    return '\n'.join(
        '{file_path}\t{file_hash}'.format(
            file_path=file_path.absolute(),
            file_hash=file_hash,
        )
        for file_path, file_hash in index.items()
    )


def hash_file_data(file_data: bytes) -> str:
    """Hash file data.

    Args:
        file_data (bytes): File data.

    Returns:
        str: File data hash.
    """
    return hashlib.sha256(file_data, usedforsecurity=False).hexdigest()


def verify_file(index: FilesIndex, file_path: Path, file_data: bytes) -> bool:
    """Verify that index contains actual file data.

    Args:
        index (FilesIndex): Files index.
        file_path (Path): File path.
        file_data (bytes): File content.

    Returns:
        bool: True if file in index and hash is same.
    """
    return index.get(file_path.absolute()) == hash_file_data(file_data)
