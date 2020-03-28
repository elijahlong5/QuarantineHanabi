from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from hanabi.config import Config

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Have to import models to resolve circular import and so migrations are
# generated for models.
from hanabi import models, routes  # noqa: F401
