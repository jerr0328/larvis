import logging
from pathlib import Path
from typing import Iterable

logger = logging.getLogger(__name__)

# A bit overengineered but also this is such a common thing


class FileCache:
    def __init__(self, max_items: int = 2, directory: Path = ".cache"):
        if max_items < 1:
            raise ValueError("max_items must be at least 1")
        self.max_items = max_items
        self.directory = Path(directory)
        self.directory.mkdir(exist_ok=True)

    @property
    def cache_size(self) -> int:
        """Get the number of files in the cache directory"""
        return len(list(self.get_files()))

    def remove_oldest(self):
        """Remove the oldest file in the cache directory"""
        # Adapted from https://realpython.com/python-pathlib/#find-the-last-modified-file
        try:
            oldest_file = min(
                (f.stat().st_mtime, f) for f in self.directory.iterdir() if f.is_file()
            )[1]
            logger.info(f"Removing {oldest_file.name}")
            oldest_file.unlink()
        except ValueError:
            logger.warning("Cannot remove anything from empty directory")

    def get_files(self) -> Iterable[Path]:
        """Iterate through all the files in the cache directory"""
        yield from (x for x in self.directory.iterdir() if x.is_file())

    def get_new_filepath(self, name: str) -> Path:
        """Return the Path to the file, ensuring cache rules are met"""
        if self.cache_size >= self.max_items:
            self.remove_oldest()

        new_file = self.directory / name
        # Touch the new file to fail-fast if the directory isn't writable
        new_file.touch()
        return new_file
