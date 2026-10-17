import subprocess

import tba

subprocess.run(["prisma", "db", "push"], check=True)
from prisma import Prisma

db = Prisma()
db.connect()


class FormParseException(Exception):
    ...


def team_get_or_create(team_number):
    team = db.team.find_unique(where={"number": team_number})
    if not team:
        team = db.team.create(data={"number": team_number})
    return team


def event_get_or_create(event_key):
    event = db.event.find_unique(where={"key": event_key})
    if not event:
        event = db.event.create(data={"key": event_key})
    return event


def match_get_or_create(event, match_code):
    match = db.match.find_unique(where={"code": match_code})
    if not match:
        match = db.match.create(data={"code": match_code, "event_key": event.key,
                                      "ordinal": tba.get_match(f"{event.key}_{match_code}").get("time", 0)})
    return match


def parse2026(form):
    event_key = f"2026{form['event_code']}"
    match_code = form['match_code']
    team_number = form["team_number"]
    form = form["form"]
    cycles = form.get("cycles")
    fuel = form.get("fuel")
    cycle_time = form.get("cycle_time")
    climb_time = form.get("climb_time")
    defense_rating = form.get("defense_rating")
    driver_rating = form.get("driver_rating")
    notes = form.get("notes")
    team = team_get_or_create(team_number)
    event = event_get_or_create(event_key)
    match = match_get_or_create(event, match_code)
    data = {
        "team_number": team.number,
        "event_key": event.key,
        "match_code": match.code
    }
    if cycles:
        data["cycles"] = cycles
    if fuel:
        data["fuel"] = fuel
    if cycle_time:
        data["cycle_time"] = int(cycle_time)
    if climb_time:
        data["climb_time"] = int(climb_time)
    if defense_rating:
        data["defense_rating"] = int(defense_rating)
    if driver_rating:
        data["driver_rating"] = int(driver_rating)
    if notes:
        data["notes"] = notes
    db.form2026.create(data=data)


_PARSERS = {2026: parse2026}


def parse_form(form):
    try:
        _PARSERS[form["year"]](form)
    except Exception as e:
        raise FormParseException(e)
