""" Routes to show apartments """
import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix

load_dotenv()

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app)

cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
# toolbar = DebugToolBarExtension(app)

if os.environ.get("FLASK_ENV") == "production":
    app.config.from_object("config.ProductionConfig")
elif os.environ.get("FLASK_ENV") == "development":
    app.config.from_object("config.DevelopmentConfig")
else:
    app.config.from_object("config.TestingConfig")

LOCAL_DEV_DB = "postgres:///apartment_ranker"

SECRET_KEY = os.environ.get("SECRET_KEY", None)

if not SECRET_KEY:
    raise Exception("Error: Set a SECRET_KEY in .env")


db = SQLAlchemy(app)
# db.app = app
# db.init_app(app)

from project.routes.routes import apartment_ranker_api

app.register_blueprint(apartment_ranker_api,
                       url_prefix="")
