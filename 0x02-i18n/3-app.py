#!/usr/bin/env python3
"""
A very basic Flask web application with internationalization support
"""
from flask import Flask
from flask import request
from flask import render_template
from flask_babel import Babel


class Config(object):
    """
    Configuration class for the application
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)


@babel.localeselector
def select_locale() -> str:
    """
    Select the best matching locale based on the request
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def display_home() -> str:
    """
    Render the home page template
    """
    return render_template('3-index.html')


if __name__ == '__main__':
    app.run()

