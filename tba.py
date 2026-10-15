import os

import dotenv
import requests

dotenv.load_dotenv()
__TBA_API_URL = "https://thebluealliance.com/api/v3"
__TBA_AUTH_HEADER = {"X-TBA-Auth-Key": os.environ["TBA_API_KEY"]}


class TBAAPIException(Exception):
    ...


def check_error(json):
    if error := json.get("Error"):
        raise TBAAPIException(error)
    return json


def get_event(event_key):
    return check_error(requests.get(f"{__TBA_API_URL}/event/{event_key}", headers=__TBA_AUTH_HEADER).json())


def get_match_keys_by_event(event_key):
    return check_error(requests.get(f"{__TBA_API_URL}/event/{event_key}/matches/keys", headers=__TBA_AUTH_HEADER).json())


def get_match(match_key):
    return check_error(requests.get(f"{__TBA_API_URL}/match/{match_key}", headers=__TBA_AUTH_HEADER).json())


def get_team(team_key):
    return check_error(requests.get(f"{__TBA_API_URL}/team/{team_key}", headers=__TBA_AUTH_HEADER).json())
