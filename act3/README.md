# Django App

## Quickstart

For quick and easy testing, just run `docker-compose up` to get everything up and running.
You can then create an admin user with `docker-compose exec web python manage.py createsuperuser` and follow the prompts.

## Deploy

Build the Docker image and deploy it where you would like. The container will start up and listen on port 8000.

## Environment Variables

- `SQL_DB`: Postgres database name
- `SQL_USER`: Database username
- `SQL_PASSWORD`: Database password
- `SQL_HOST`: Database server hostname
- `SQL_PORT`: Database server port (default: 5432)
- `DEBUG`: Set to true to enable debug mode
- `DJANGO_SECRET_KEY`: Set the Django secret key (set this when running in production!)


## Solution considerations, future improvements

I've set up several Django projects before, but all of them using Django Rest Framework (DRF), so this one I needed to figure out a bit how the templating really works to make an easy frontend. I didn't add DRF here since I don't have anything to consume it, so I didn't want to bring in more complexity.

The settings and configuration are mostly defaults. I added some environment variable control, but of course all the headers and content security policies to make Mozilla Observatory green would need to be done. There are useful guides on this, but it felt out of scope as I don't intend on deploying this publicly.

My HTML/CSS skills are extremely dated, but I did know enough to use Materialize for some "free" styling help to not look so bland. As mentioned above, I would rather use DRF on the backend and deploy a static website somewhere like S3 to take advantage of a CDN, rather than rendering on the backend, but this was not really in the scope of the challenge. If I had any design sense, I would like to make it prettier.
