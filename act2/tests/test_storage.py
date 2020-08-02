from pathlib import Path

from act2 import storage


def test_empty_file_cache(tmp_path: Path):
    cache = storage.FileCache(directory=tmp_path)
    assert cache.cache_size == 0
    assert list(cache.get_files()) == []
    cache.remove_oldest()  # No exception thrown


def test_file_cache_create(tmp_path: Path):
    subdir = tmp_path / "sub"
    assert not subdir.exists()
    storage.FileCache(directory=subdir)
    assert subdir.exists()


def test_file_cache_filling(tmp_path: Path):
    cache = storage.FileCache(directory=tmp_path, max_items=2)
    assert cache.cache_size == 0
    first_path = cache.get_new_filepath("1")
    assert cache.cache_size == 1
    second_path = cache.get_new_filepath("2")
    assert cache.cache_size == 2
    assert sorted(cache.get_files()) == [first_path, second_path]
    third_path = cache.get_new_filepath("3")
    assert cache.cache_size == 2
    assert sorted(cache.get_files()) == [second_path, third_path]
