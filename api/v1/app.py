#!/usr/bin/python3

from flask import Flask
from models import storage
from api.v1.views import app_views
from os import getenv

HBNB_API_HOST = getenv('HBNB_API_HOST', '0.0.0.0')
HBNB_API_PORT = getenv('HBNB_API_PORT', 5000)


app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def db_close(self):
    """
    close the storage on close down
    """
    storage.close()


if __name__ == "__main__":
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
