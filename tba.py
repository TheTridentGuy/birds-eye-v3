import os
import requests
import dotenv


dotenv.load_dotenv()
__TBA_API_URL = "https://thebluealliance.com/api/v3"
__TBA_AUTH_HEADER = {"X-TBA-Auth-Key": os.environ["TBA_API_KEY"]}


def get_events_by_year(year):
    return requests.get(f"{__TBA_API_URL}/{year}/events", headers=__TBA_AUTH_HEADER).text


def get_matches_by_event_json(event_key):
    return requests.get(f"{__TBA_API_URL}/event/{event_key}/matches", headers=__TBA_AUTH_HEADER).text


def get_match_json(match_key):
    return requests.get(f"{__TBA_API_URL}/match/{match_key}", headers=__TBA_AUTH_HEADER).text


def get_team_json(team_key):
    return requests.get(f"{__TBA_API_URL}/team/{team_key}", headers=__TBA_AUTH_HEADER).text
