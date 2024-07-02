#!/usr/bin/env python3
"""
A minimal Flask application utilizing Babel for i18n
"""
from flask import Flask
from flask import request
from flask import render_template
from flask_babel import Babel


class Config(object):
    """
    Application configuration class
    """
    LANGUAGES: list[str] = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


app = Flask(__name__)
app.config.from_object(Config)

babel = Babel(app)


@babel.localeselector
def select_locale() -> str:
    """
    Selects locale based on request
    """
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def display_template() -> str:
    """
    Renders a basic html template
    """
    return render_template('2-index.html')


if __name__ == '__main__':
    app.run()
