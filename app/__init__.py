from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)
# Handles all migrations.
migrate = Migrate(app, db)

app.secret_key = "351d72e2ebe8156fe595e99f35d918fd64a243582b4bf162656df383dd9246c2"

login_manager = LoginManager()
login_manager.init_app(app)

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s | %(levelname)s | %(message)s")

from app import views, models