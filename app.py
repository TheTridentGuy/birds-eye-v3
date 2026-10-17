import datetime
import logging
import os
import re

import dotenv
from flask import Flask, redirect, render_template, request
from jinja2 import TemplateNotFound

import parse
import tba

app = Flask(__name__)
logger = logging.getLogger(__name__)
dotenv.load_dotenv()
FEATURED_EVENTS = os.environ.get("FEATURED_EVENTS", "").split(",")


@app.route("/")
def index():
    return redirect(f"/{datetime.datetime.now().year}")


@app.errorhandler(tba.TBAAPIException)
def tba_api_exception(e):
    logger.error(f"TBAAPIException: {e}")
    return "The TBA API returned an error. You probably asked for something that doesn't exist.", 400


@app.route("/<int:year>")
def events_by_year(year):
    featured_events = [tba.get_event(f"{year}{event}") for event in FEATURED_EVENTS]
    return render_template("events_by_year.html", year=year, featured_events=featured_events)


@app.route("/<int:year>/<event_code>")
def matches_by_event(year, event_code):
    event_key = f"{year}{event_code}"
    event = tba.get_event(event_key)
    match_keys = [match_key.split("_")[1] for match_key in tba.get_match_keys_by_event(event_key)]
    match_keys.sort(key=lambda c: (
        {"pm": 0, "qm": 1, "ef": 2, "qf": 3, "sf": 4, "f": 5}.get(re.match(r"[a-z]*", c.lower())[0], 9),
        *map(int, re.findall(r"\d+", c)),
    ))
    return render_template("matches_by_event.html", year=year, event=event, match_keys=match_keys)


@app.route("/<int:year>/<event_code>/<match_key>")
def team_by_match(year, event_code, match_key):
    match = tba.get_match(f"{year}{event_code}_{match_key}")
    blue_alliance = [tba.get_team(team_key.strip("B")) for team_key in match["alliances"]["blue"]["team_keys"]]
    red_alliance = [tba.get_team(team_key.strip("B")) for team_key in match["alliances"]["red"]["team_keys"]]
    return render_template("team_by_match.html", year=year, event_code=event_code, match_key=match_key,
                           blue_alliance=blue_alliance, red_alliance=red_alliance)


@app.route("/<int:year>/<event_code>/<match_code>/<int:team_number>", methods=["GET", "POST"])
def scout(year, event_code, match_code, team_number):
    if request.method == "GET":
        team = tba.get_team(f"frc{team_number}")
        try:
            return render_template(f"scout{year}.html", year=year, event_code=event_code, match_code=match_code,
                                   team_number=team_number, team=team)
        except TemplateNotFound:
            return f"No form for {year}.", 404
    else:
        assert request.method == "POST"
        try:
            parse.parse_form(request.json)
            return ""
        except parse.FormParseException as e:
            logger.error(f"FormParseException: {e}")
            logger.error(request.json)
            return "Error parsing form. See logs for details.", 400
