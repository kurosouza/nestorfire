from flask import Flask
from nestorfire.adapters.http.endpoints import bp
import os

def create_app():
    app = Flask(__name__)
    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)
    app.register_blueprint(bp)
    return app
