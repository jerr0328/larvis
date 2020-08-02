# LARVIS

A three-part challenge. This was quite fun. You can find further information in each directory.

All three acts can be run in the same virtualenv. I ran in Python 3.8.5 on macOS.
Once the virtualenv is set up, run `pip install -r requirements-dev.txt` to install shared development requirements.

Pre-commit hooks should also be installed when making changes: `pre-commit install`

You can run tests for Acts 1 and 2 by running `pytest -v`.

Act 3 is self-contained, so commands and imports are relative to the `act3` directory (unlike others which are relative to this directory).
