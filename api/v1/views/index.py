#!/usr/bin/python3

"""
creates route /status for blueprint object app_views
"""

from api.v1.views import app_views

@app_views.route("/status")
def get_status():
    """
    Returns the status code
    """
    return {
        "status": "OK"
    }
    