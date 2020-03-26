# The base image for the application containing all required dependencies.
FROM python:3.7 AS dependencies

WORKDIR /opt/hanabi

# Flask application specified as '[path/to/]module[.submodule][:member]'
ENV FLASK_APP=run

# Install dependencies. We only copy the requirements.txt file so that the
# dependency layer can be cached even if the rest of the application code
# changes.
COPY requirements.txt .
RUN pip install -r requirements.txt


# Image for development
FROM dependencies AS devserver

# Flask runs the server on port 5000
EXPOSE 5000

ENV FLASK_ENV=development

# Copy in our application code. Note that this is the last (work-intensive) step
# so that we can get the most out of layer caching.
COPY . .

ENTRYPOINT ["flask", "run", "--host=0.0.0.0"]


# Production image
FROM dependencies

# Run on the expected port for HTTP services
EXPOSE 80

ENV FLASK_ENV=production

RUN pip install gunicorn==20.0.4

COPY . .

ENTRYPOINT ["gunicorn", "-w", "4", "-b", "0.0.0.0:80", "run:app"]
