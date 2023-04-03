# Base image for container image
FROM python:3.10-slim-bullseye

# Docker image is built layer by layer, so subsequent commands are run on top of previous changes
# --no-cache is for minimizing container weight and to avoid dependencies packages vulnerabilities
RUN apt-get update \
  && apt-get install -y --no-install-recommends --no-install-suggests \
  build-essential default-libmysqlclient-dev \
  && pip install --no-cache-dir --upgrade pip

WORKDIR /app
# It is in the separate line, so if only requirements file changes, only this layer will be updated. Layers use cache.
COPY ./requirements.txt /app 
RUN pip install --no-cache-dir --requirement /app/requirements.txt
# If only app changes, then only following layers will change:
COPY . /app

EXPOSE 5000

CMD ["python3", "server.py"]