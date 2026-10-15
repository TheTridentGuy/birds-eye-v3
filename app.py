import datetime
import logging
import os
import dotenv
from flask import Flask, redirect

app = Flask(__name__)
logger = logging.getLogger(__name__)
dotenv.load_dotenv()
FEATURED_EVENTS = os.environ.get("FEATURED_EVENTS", "").split(",")


@app.route("/")
def index():
    return redirect(f"/{datetime.datetime.now().year}")


@app.route("/<int:year>")
def events_by_year(year):
    if not 1900 < year < 9999:
        return "Invalid year.", 400
    for event in FEATURED_EVENTS:
        event_key = f"{year}{event}"
    return ""
