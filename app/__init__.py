from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_babel import Babel
import logging

def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'en')

app = Flask(__name__)
app.config.from_object('config')
app.secret_key = "351d72e2ebe8156fe595e99f35d918fd64a243582b4bf162656df383dd9246c2"

db = SQLAlchemy(app)
# Handles all migrations.
migrate = Migrate(app, db)

login_manager = LoginManager()
login_manager.session_protection = True
login_manager.init_app(app)

logging.basicConfig(level=logging.DEBUG, 
                    format="%(asctime)s | %(levelname)s | %(message)s", 
                    filemode='a', 
                    filename='logs/tunes.io.log', 
                    encoding='utf-8')

from app import views, login_endpoints, ajax_endpoints, models