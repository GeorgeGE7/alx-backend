#!/usr/bin/env python3
"""
A web application with internationalization using Flask and Babel
"""
from flask import Flask
from flask import request
from flask import render_template
from flask_babel import Babel


class Config(object):
    """
    Configuration class for the web application
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
    Selects the preferred locale from the request
    """
    locale = request.args.get('locale', '').strip()
    if locale and locale in Config.LANGUAGES:
        return locale
    return request.accept_languages.best_match(app.config['LANGUAGES'])


@app.route('/', strict_slashes=False)
def home() -> str:
    """
    Renders the home page
    """
    return render_template('4-index.html')


if __name__ == '__main__':
    app.run()
