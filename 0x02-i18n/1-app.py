#!/usr/bin/env python3
"""
A very basic Flask web application
"""
from flask import Flask
from flask import render_template
from flask_babel import Babel


class AppConfig(object):
    """
    Application configuration class
    """
    LANGUAGES = ['en', 'fr']
    BABEL_DEFAULT_LOCALE = 'en'
    BABEL_DEFAULT_TIMEZONE = 'UTC'


# Create the application object
web_app = Flask(__name__)
web_app.config.from_object(AppConfig)

# Wrap the application with Babel
locale_manager = Babel(web_app)


@web_app.route('/', strict_slashes=False)
def main_page() -> str:
    """
    Renders the main page
    """
    return render_template('1-index.html')


if __name__ == '__main__':
    web_app.run()


