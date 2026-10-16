import datetime
import logging
import os

import dotenv
from flask import Flask, redirect, render_template, request
from jinja2 import TemplateNotFound

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
    return render_template("matches_by_event.html", year=year, event=event, match_keys=match_keys)


@app.route("/<int:year>/<event_code>/<match_key>")
def team_by_match(year, event_code, match_key):
    match = tba.get_match(f"{year}{event_code}_{match_key}")
    blue_alliance = [tba.get_team(team_key) for team_key in match["alliances"]["blue"]["team_keys"]]
    red_alliance = [tba.get_team(team_key) for team_key in match["alliances"]["red"]["team_keys"]]
    return render_template("team_by_match.html", year=year, event_code=event_code, match_key=match_key, blue_alliance=blue_alliance, red_alliance=red_alliance)


@app.route("/<int:year>/<event_code>/<match_key>/<int:team_number>", methods=["GET", "POST"])
def scout(year, event_code, match_key, team_number):
    if request.method == "GET":
        match = tba.get_match(f"{year}{event_code}_{match_key}")
        team = tba.get_team(f"frc{team_number}")
        print(match)
        try:
            return render_template(f"scout{year}.html", year=year, event_code=event_code, match_key=match_key, team_number=team_number, team=team)
        except TemplateNotFound:
            return f"No form for {year}.", 404
    else:
        assert request.method == "POST"
        print(request.json)
        return ""
