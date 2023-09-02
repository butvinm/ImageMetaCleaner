"""Files index module.

This module contains functions for creating and reading files index
with information about processed files.
"""


import hashlib
from pathlib import Path
from typing import Iterator, Mapping, MutableMapping, Optional


def hash_file_data(file_data: bytes) -> str:
    """Hash file data.

    Args:
        file_data (bytes): File data.

    Returns:
        str: File data hash.
    """
    return hashlib.sha256(file_data, usedforsecurity=False).hexdigest()


class FilesIndex(MutableMapping[Path, str]):  # noqa: WPS214
    """Files index with processed files content hash."""

    def __init__(
        self,
        initial_dict: Optional[Mapping[Path, str]] = None,
    ) -> None:
        """Init index data.

        Args:
            initial_dict (Optional[Mapping[Path, str]]): \
                Initial index data.
        """
        self._files_hashes: dict[Path, str] = {}
        if initial_dict is not None:
            self._files_hashes.update({
                file_path.absolute(): file_hash
                for file_path, file_hash in initial_dict.items()
            })

    def __getitem__(self, file_path: Path) -> str:
        """Get file hash by path.

        Path is casted to absolute format.

        Args:
            file_path (Path): File path.

        Returns:
            str: File hash if file exists.
        """
        return self._files_hashes[file_path.absolute()]

    def __setitem__(self, file_path: Path, file_hash: str) -> None:
        """Set hash for file path.

        File path is casted to absolute format.

        Args:
            file_path (Path): File path.
            file_hash (str): File content hash.
        """
        self._files_hashes[file_path.absolute()] = file_hash

    def __delitem__(self, file_path: Path) -> None:  # noqa: WPS603
        """Remove file path from index.

        File path is casted to absolute format.

        Args:
            file_path (Path): File path.
        """
        self._files_hashes.pop(file_path.absolute())

    def __iter__(self) -> Iterator[Path]:
        """Return iterator over consisted files pathes.

        Returns:
            Iterator[Path]: Iterator over files pathes
        """
        return iter(self._files_hashes)

    def __len__(self) -> int:
        """Return count of files in index.

        Returns:
            int: Count of files in index.
        """
        return len(self._files_hashes)

    def __repr__(self) -> str:
        """Return repr of internal files hashes map.

        Returns:
            str: Repr of files index.
        """
        return repr(self._files_hashes)

    def add_file(self, file_path: Path, file_data: bytes) -> str:
        """Add file to index.

        File path is casted to absolute format and
        file data is hashed with `hash_file_data` function.

        Args:
            file_path (Path): File path.
            file_data (bytes): File content.

        Returns:
            str: Hashed file data.
        """
        file_hash = hash_file_data(file_data)
        self._files_hashes[file_path.absolute()] = file_hash
        return file_hash

    def verify_file(self, file_path: Path, file_data: bytes) -> bool:
        """Verify that index contains actual file data.

        Args:
            file_path (Path): File path.
            file_data (bytes): File content.

        Returns:
            bool: True if file in index and hash is same.
        """
        return self.get(file_path) == hash_file_data(file_data)

    def build_index_file(self) -> str:
        """Build content of index file.

        Index file contains absolute pathes to files with
        hashes separated with tabulation.

        Returns:
            str: Index files content
        """
        return '\n'.join(
            '{file_path}\t{file_hash}'.format(
                file_path=file_path.absolute(),
                file_hash=file_hash,
            )
            for file_path, file_hash in self._files_hashes.items()
        )

    @classmethod
    def from_index_file(cls, file_data: str) -> 'FilesIndex':
        """Build FilesIndex object from index file.

        Args:
            file_data (str): Content of index file.

        Returns:
            FilesIndex: New index object.
        """
        index = FilesIndex()
        for line in file_data.splitlines():
            if line:
                file_path, file_hash = line.split('\t')
                index[Path(file_path)] = file_hash

        return index
