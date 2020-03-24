# QuarantineHanabi

## Developer Setup

After cloning the project, the first step is to create a Python 3.7 virtual
environment that the project can use. This environment *MUST* be named
`quarantine-hanabi`.

```bash
# Assuming you have virtualenv-wrapper
mkvirtualenv --python python3.7 quarantine-hanabi
```

The next step is to install the developer hooks responsible for autoformatting
and linting before each commit:

```bash
workon quarantine-hanabi
pip install -r requirements.txt
pre-commit install
```
