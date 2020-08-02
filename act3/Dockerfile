# Basically the sample Dockerfile
FROM python:3.8

# Needed for finding out if postgres is up and running
RUN apt-get -q update \
    && apt-get -qy install --no-install-recommends \
    netcat \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /usr/src/app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "gunicorn", "worldsaving.wsgi:application", "--bind=0.0.0.0:8000"]
