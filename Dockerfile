# Pull the python image
FROM python:3.10.14-alpine

# Update the system
RUN apk update
RUN apk upgrade

RUN apk add \
    build-base \
    postgresql \
    postgresql-dev \
    libpq \
    ffmpeg

# Environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Create entrypoint directory
RUN mkdir /usr/src/entrypoint
WORKDIR /usr/src/entrypoint
COPY ./docker-entrypoint.sh .
COPY ./admin-creator.py .
RUN chmod +x docker-entrypoint.sh

# Create working directory
RUN mkdir /usr/src/app
WORKDIR /usr/src/app

# Install python dependencies
COPY ./requirements.txt .
RUN pip install -r requirements.txt
RUN rm -f requirements.txt

# Create Entrypoint Hook
ENTRYPOINT ["/usr/src/entrypoint/docker-entrypoint.sh"]
