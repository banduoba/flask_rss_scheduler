from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from config import Config

app = Flask(__name__)

app.config.from_object(Config)
app.config['PERMANENT_SESSION_LIFETIME'] = 60 * 60 * 24
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from app import web, models
