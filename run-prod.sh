#!/bin/bash
FLASK_APP=app.server
env/bin/gunicorn -w 2 app.server:app
