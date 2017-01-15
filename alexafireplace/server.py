# Defines the Alexa Fireplace Server

from flask import Flask
from flask import render_template
from flask_migrate import Migrate
from flask_oauthlib.provider import OAuth2Provider
from flask_sqlalchemy import SQLAlchemy

# Load and configure the Flask Application
app = Flask(__name__)
app.config.from_object('alexafireplace.config')
db = SQLAlchemy(app)
migrate = Migrate(app, db)
oauth = OAuth2Provider(app)


# Import Views and Models
from alexafireplace import models
from alexafireplace import views


# Provide a basic Index page, primarily as a debug heartbeat
@app.route('/')
def index():
    """Renders and returns the Alexa Fireplace index page."""
    return render_template('index.jinja')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8080")
