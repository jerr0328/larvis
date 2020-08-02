# XKCD Service

## Install

1. Install python3 (tested with Python 3.8)
2. Run `pip install -r requirements.txt` to install dependencies

## Run locally

To test-run the service, you can invoke it by calling `python3 -m act2.xkcd` from the parent directory.
It will create the `xkcd` directory and store the files there.

## Configuration

Set the `XKCD_COMICS_DIR` environment variable to the path where the XKCD comics will live.
If the directory doesn't exist, it will be automatically created. By default it will use `xkcd` in the current directory.

**Note** that the service will ensure there's only up to 2 files in there (per spec)
so make sure to not point it at an important directory.

## Set up systemd service

1. Depending on where this is installed on the OS, change the `xkcd.service` file to use the correct paths and users.
The following should be set depending on the specific installation:
- `User` - Set to a non-root user (e.g. `pi` on a Raspberry Pi).
- `WorkingDirectory` - Set to the directory where the repo was cloned (e.g. `/home/pi/larvis`).
- `Environment=XKCD_COMICS_DIR` - Set to a directory where the XKCD comics will be stored (see "Configuration" above).

2. Once properly configured, copy the `xkcd.service` and `xkcd.timer` files to `/etc/systemd/system` (using sudo).
3. Run `sudo systemctl daemon-reload` to load the configuration
4. Enable the timer with `sudo systemctl enable xkcd.timer`.

## Kubernetes CronJob

If you are running this on a Kubernetes cluster, build the Docker image and push to a registry,
then edit the `kube-cronjob.yaml` file with the correct image name and persistent volume name.

## Solution considerations, future improvements

The solution here handles errors in a very lazy way by simply propogating them, as we can let the system restart the service and hopefully clear the problem.

There are plenty of ways to handle periodic tasks. For instance, you can have a constantly-running program that relies on the `schedule` package (but then you have to keep the application running continuously, which isn't great for anything happening less frequently than once a minute) or you can use the system crontab. You can use celery beat if you have that infrastructure set up as well. My assumption is that it will either run in a modern Linux system with systemd or on a modern-enough Kubernetes cluster where the beta "CronJob" type is available.

Storage management is a key factor in this one, so ensuring only two comics are in the cache at a time needed a little handler to abstract most of that logic from the comic-fetching logic. I searched quickly for some generic LRU file caches, but a lot of them are focused more on function call results than actual files.

One improvement I would likely make would be to use `click` to make a full CLI tool out of this and better handle the destination folder (rather than just using an environment variable).
Also, making this a PyPi package (with setup.py or pyproject.toml) would allow the use of a console script, and I could then use similar instructions as my CO2 monitor: https://github.com/jerr0328/co2mini.
