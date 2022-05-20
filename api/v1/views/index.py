#!/usr/bin/python3
"""verifies status on json object"""

from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def objStatus():
    """status of obj app_views returned as JSON"""
    return jsonify({"status": "OK"})
