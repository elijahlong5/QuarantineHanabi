# QuarantineHanabi

## IDE Setup

After cloning the project, the first step is to create a Python 3.7 virtual
environment that the project can use. This environment *MUST* be named
`quarantine-hanabi`.

```bash
# Assuming you have virtualenv-wrapper
mkvirtualenv --python python3.7 quarantine-hanabi
```

The next step is to install the developer hooks responsible for auto-formatting
and linting before each commit:

```bash
workon quarantine-hanabi
pip install -r requirements.txt
pre-commit install
```

## Development Server

To spin up a development environment, use [`docker-compose`][docker-compose]:

```bash
docker-compose up

# If you wish to run the services in the background, add the `-d` flag.
docker-compose up -d
```

If you do run the development environment in the background, it can be stopped
or destroyed with the following commands:

```bash
# To stop the containers
docker-compose stop

# To destroy all the associated resources:
docker-compose down
```

### IntelliJ

There is a "Dev Environment" run configuration provided by the project that can
be run in IntelliJ to manage the development environment.

[docker-compose]: https://docs.docker.com/compose/
