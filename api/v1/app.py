#!/usr/bin/python3
"""first endpoint returns status of API"""

from os import getenv
from models import storage
from api.v1.views import app_views
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app, resources={"/*": {"origins": '0.0.0.0'}})
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(code):
    """teardown_appcontext"""
    storage.close()


@app.errorhandler(404)
def page_not_found(code):
    return jsonify({
        "error": "Not found"
    }), 404


if __name__ == "__main__":
    PORT = getenv("HBNB_API_PORT", '8080')
    HOST = getenv("HBNB_API_HOST", '0.0.0.0')
    app.run(host=HOST, port=PORT, threaded=True)
