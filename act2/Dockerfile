# Basically the sample Dockerfile
FROM python:3.8-slim

WORKDIR /usr/src/app

COPY requirements.txt act2/
RUN pip install --no-cache-dir -r act2/requirements.txt

COPY . act2/

CMD [ "python3", "-m", "act2.xkcd" ]
