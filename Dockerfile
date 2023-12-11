# Use an official Python runtime as a parent image
FROM python:3.10.12

RUN apt-get -y update \
  && apt-get install -y gettext \
  # Cleanup apt cache
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the pyproject.toml and poetry.lock files into the container at /app
COPY pyproject.toml poetry.lock /app/

# Install Poetry and project dependencies
RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-dev

# Copy the current directory contents into the container at /app
COPY . /app/

# Collect static files
#RUN python manage.py collectstatic --noinput

# Make port 8000 available to the world outside this container
EXPOSE 8000

# Define the command to run on container start
CMD ["gunicorn", "--bind", "0.0.0.0:1000", "simple_wallet.wsgi:application"]
