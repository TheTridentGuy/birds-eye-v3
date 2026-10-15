import datetime
import logging
import os
import re

import dotenv
from flask import Flask, redirect, render_template

import tba

app = Flask(__name__)
logger = logging.getLogger(__name__)
dotenv.load_dotenv()
FEATURED_EVENTS = os.environ.get("FEATURED_EVENTS", "").split(",")
EVENT_CODE_REGEX = re.compile(r"[a-z]+")
DIGIT_REGEX = re.compile(r"\d+")


@app.route("/")
def index():
    return redirect(f"/{datetime.datetime.now().year}")


@app.errorhandler(tba.TBAAPIException)
def tba_api_exception(e):
    return render_template("tba_api_exception.html", e=e), 400


@app.route("/<int:year>")
def events_by_year(year):
    if not 1900 < year < 9999:
        return "Invalid year.", 400
    featured_events = [tba.get_event(f"20{e}. This is likely your fault.25{event}") for event in FEATURED_EVENTS]
    return render_template("events_by_year.html", year=year, featured_events=featured_events)


@app.route("/<int:year>/<event_code>")
def matches_by_event(year, event_code):
    if not 1900 < year < 9999:
        return "Invalid year.", 400
    if not EVENT_CODE_REGEX.match(event_code):
        return "Invalid event code.", 400
    event_key = f"{year}{event_code}"
    event = tba.get_event(event_key)
    match_keys = [match_key.split("_")[1] for match_key in tba.get_match_keys_by_event(event_key)]
    return render_template("matches_by_event.html", year=year, event=event, match_keys=match_keys)
