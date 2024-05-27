#!/usr/bin/python3
"""
creates route /status for blueprint object app_views
"""

from api.v1.views import app_views
from models import storage


@app_views.route("/status")
def get_status():
    """
    Returns the status code
    """
    return {
        "status": "OK"
    }


@app_views.route("/stats")
def get_stats():
    """
    Returns the stats of each objects
    """
    stats = {}
    for key, cls in storage.get_classes().items():
        class_count = storage.count(cls)
        stats[cls.__tablename__] = class_count
    return stats
