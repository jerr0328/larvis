"""
Fun-fact, I made something similar in the past to pull gallery images from Planet
which I had point to a folder that was used to randomly change my desktop background:
https://github.com/jerr0328/pl-gallery-grabber
The code is old and there's a lot I could have done better,
and is archived since the gallery stopped being updated and I didn't want to maintain it.
"""

import logging
import os
import random
import shutil
from pathlib import Path

import requests

from .storage import FileCache

XKCD_COMICS_DIR = Path(os.getenv("XKCD_COMICS_DIR", "xkcd"))
# If we really need to roll randomness more than 3 times, something's not right
MAX_RANDOM_ITERATIONS = 3

cache = FileCache(max_items=2, directory=XKCD_COMICS_DIR)
logger = logging.getLogger(__name__)


class RandomnessException(Exception):
    pass


def get_latest_comic_number() -> int:
    """Return the most recent comic number

    Note that if API is down or changes, exceptions will be raised
    """
    r = requests.get("https://xkcd.com/info.0.json")
    r.raise_for_status()
    return r.json()["num"]


def comic_already_exists(comic_number: int) -> bool:
    return any(x.name.startswith(f"{comic_number}.") for x in cache.get_files())


def get_new_random_comic_number(latest_comic_number: int) -> int:
    """Get a new comic that we haven't fetched before.

    Not chosen by dice roll: https://xkcd.com/221/
    """

    # Loop until we find a new comic, hopefully only once
    for _ in range(MAX_RANDOM_ITERATIONS):
        random_number = random.randint(1, latest_comic_number)
        if not comic_already_exists(random_number):
            return random_number
    else:
        # Note this else belongs to the `for` loop, in case we didn't break out of the loop
        raise RandomnessException(
            f"Could not generate a random comic after {MAX_RANDOM_ITERATIONS} iterations"
        )


def get_comic_metadata(comic_number: int) -> dict:
    r = requests.get(f"https://xkcd.com/{comic_number}/info.0.json")
    r.raise_for_status()  # in case of 404, as with comic 404
    return r.json()


def download_comic(comic_number):
    metadata = get_comic_metadata(comic_number)
    logger.debug(f"Fetching comic {comic_number} called: {metadata.get('title', '')}")
    suffix = Path(metadata["img"]).suffix  # may be .png or .jpg
    new_file_path = cache.get_new_filepath(f"{comic_number}{suffix}")
    # Based on: https://stackoverflow.com/a/39217788/375530
    with requests.get(metadata["img"], stream=True) as r:
        r.raise_for_status()
        logger.debug(f"Downloading to {new_file_path}")
        with new_file_path.open("wb") as f:
            shutil.copyfileobj(r.raw, f)

    return new_file_path


def fetch_random_comic() -> Path:
    latest_comic_number = get_latest_comic_number()
    logger.debug(f"Newest comic is {latest_comic_number}")
    random_comic_number = get_new_random_comic_number(latest_comic_number)
    logger.info(f"Fetching comic: {random_comic_number}")
    return download_comic(random_comic_number)


if __name__ == "__main__":
    fetch_random_comic()
