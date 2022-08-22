#!/usr/bin/env python
#

import json
import logging

from flask import Flask, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from flask_debugtoolbar import DebugToolbarExtension


from pignus_api.controllers.ctrl_models.ctrl_image import ctrl_image
from pignus_api.controllers.ctrl_collections.ctrl_images import ctrl_images
from pignus_api.utils import db
from pignus_api.utils import glow
from pignus_api.utils import date_utils
from pignus_api.collections.options import Options

app = Flask(__name__)
app.config.update (
    DEBUG = True,
)
app.config['SECRET_KEY'] = "test"
toolbar = DebugToolbarExtension(app)

glow.db = db.connect()
glow.options = Options().load_options()



def register_blueprints(app: Flask):
    """Connect the blueprints to the router."""
    app.register_blueprint(ctrl_image)
    app.register_blueprint(ctrl_images)
    return True


@app.route('/')
def index():
    print(date_utils.now())
    with glow.db.cursor() as cursor:
        # Read a single record
        sql = "SELECT * FROM `users`;"
        cursor.execute(sql)
        result = cursor.fetchone()
        print(result)

    data = {
        'info': "Pignus Api",
        "version": "0.0.1"
    }
    return jsonify(data)


@app.route('/debug')
def debug():
    html = "<html><head><title>debug</title></head><body></body></html>"
    return html



if __name__ == "__main__":
    register_blueprints(app)
    app.run(host='0.0.0.0', port=5001)

elif __name__ != '__main__':
    register_blueprints(app)
    gunicorn_logger = logging.getLogger('gunicorn.info')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)


# End File: pignus/src/pignus_api/app.py
