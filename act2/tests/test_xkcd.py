from pathlib import Path

import pytest
import requests

from act2 import xkcd


def test_get_latest_comic_number(requests_mock):
    requests_mock.get("https://xkcd.com/info.0.json", json={"num": 1151})
    assert xkcd.get_latest_comic_number() == 1151


def test_get_comic_metadata(requests_mock):
    # Comic 404 doesn't actually exist, so good way to assert that the mock works.
    mock_metadata = {
        "num": 404,
        "img": "https://www.explainxkcd.com/wiki/images/9/92/not_found.png",
    }
    requests_mock.get("https://xkcd.com/404/info.0.json", json=mock_metadata)
    assert xkcd.get_comic_metadata(404) == mock_metadata


def test_get_comic_metadata_404(requests_mock):
    requests_mock.get("https://xkcd.com/404/info.0.json", status_code=404)
    with pytest.raises(requests.HTTPError):
        xkcd.get_comic_metadata(404)


def test_comic_already_exists(mocker):
    # Pretend there's already the first comic in the cache
    mock_cache_get_files = mocker.patch("act2.xkcd.cache.get_files")
    mock_cache_get_files.return_value = [Path("1.jpg")]
    # First comic in the cache
    assert xkcd.comic_already_exists(1)
    # Second comic not in the cache
    assert not xkcd.comic_already_exists(2)


def test_get_new_random_comic_number_broken_random(mocker):
    # Pretending no matter what, the comic exists. Should raise exception
    mock_comic_already_exists = mocker.patch("act2.xkcd.comic_already_exists")
    mock_comic_already_exists.return_value = True
    with pytest.raises(xkcd.RandomnessException):
        xkcd.get_new_random_comic_number(100)
    assert mock_comic_already_exists.call_count == xkcd.MAX_RANDOM_ITERATIONS


def test_get_new_random_comic_number_retry(mocker):
    # First number would exist already, second number not
    mock_comic_already_exists = mocker.patch("act2.xkcd.comic_already_exists")
    mock_comic_already_exists.side_effect = [True, False]
    mock_random = mocker.patch("act2.xkcd.random.randint")
    mock_random.side_effect = [221, 4]
    assert xkcd.get_new_random_comic_number(3000) == 4
    assert mock_comic_already_exists.call_count == 2


def test_download_comic(mocker, requests_mock, tmp_path):
    # This isn't a great test because it's mostly mocks, but still proves the logic flow
    fake_img_url = "https://fake.url/sample.txt"
    fake_comic_number = 404
    expected_generated_file = "404.txt"
    expected_file_contents = "Sample"
    # Mock request so img download is tested
    requests_mock.get(fake_img_url, text=expected_file_contents)
    # Mock metadata response to have our fake URL inserted
    mock_metadata = mocker.patch("act2.xkcd.get_comic_metadata")
    mock_metadata.return_value = {"img": fake_img_url, "title": "Fake comic"}
    # Mock cache to have temporary path from pytest
    mock_cache = mocker.patch("act2.xkcd.cache.get_new_filepath")
    mock_cache.return_value = tmp_path / expected_generated_file

    comic_path = xkcd.download_comic(fake_comic_number)
    assert comic_path.read_text() == expected_file_contents
    assert mock_cache.call_args == ((expected_generated_file,),)
    assert mock_metadata.call_args == ((fake_comic_number,),)
