# The base image for the application containing all required dependencies.
FROM python:3.7 AS dependencies

ENV PYTHONDONTWRITEBYTECODE=true

WORKDIR /opt/hanabi

# Install dependencies. We only copy the requirements.txt file so that the
# dependency layer can be cached even if the rest of the application code
# changes.
COPY requirements.txt .
RUN pip install -r requirements.txt


# Image for development
FROM dependencies AS devserver

# Default port for Django devserver
EXPOSE 8000

ENV DEBUG=True

# Copy in our application code. Note that this is the last (work-intensive) step
# so that we can get the most out of layer caching.
COPY . .

ENTRYPOINT ["hanabi/manage.py", "runserver", "0.0.0.0:8000"]


# Production image
FROM dependencies

# Run on the expected port for HTTP services
EXPOSE 80

RUN pip install gunicorn==20.0.4

COPY . .

WORKDIR ./hanabi

ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "hanabi.wsgi:application"]
