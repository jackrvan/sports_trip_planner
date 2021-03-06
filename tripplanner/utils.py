import sys
import os
import requests

COUNTRY_CHOICES = {
    ("CA", "Canada"),
    ("US", "USA"),
}
PROVINCES = {
    "Canada": [
        "Alberta",
        "British Columba",
        "Manitoba",
        "New Brunswick",
        "Newfoundland and Labrador",
        "Northwest Territories",
        "Nova Scotia",
        "Nunavut",
        "Ontario",
        "Prince Edward Island",
        "Quebec",
        "Saskatchewan",
        "Yukon",
    ],
    "USA": [
        "Alabama",
        "Alaska",
        "Arizona",
        "Arkansas",
        "California",
        "Colorado",
        "Connecticut",
        "Delaware",
        "Florida",
        "Georgia",
        "Hawaii",
        "Idaho",
        "Illinois",
        "Indiana",
        "Iowa",
        "Kansas",
        "Kentucky",
        "Louisiana",
        "Maine",
        "Maryland",
        "Massachusetts",
        "Michigan",
        "Minnesota",
        "Mississippi",
        "Missouri",
        "Montana",
        "Nebraska",
        "Nevada",
        "New Hampshire",
        "New Jersey",
        "New Mexico",
        "New York",
        "North Carolina",
        "North Dakota",
        "Ohio",
        "Oklahoma",
        "Oregon",
        "Pennsylvania",
        "Rhode Island",
        "South Carolina",
        "South Dakota",
        "Tennessee",
        "Texas",
        "Utah",
        "Vermont",
        "Virginia",
        "Washington",
        "West Virginia",
        "Wisconsin",
        "Wyoming",
    ]
}

"""
def get_games(team_name):
    all_teams = requests.get("https://statsapi.web.nhl.com/api/v1/teams").json()
    team_id = next(team['id'] for team in all_teams['teams'] if team['name'] == team_name)
    params = {'teamId': team_id, 'startDate': '2021-02-05', 'endDate': '2021-02-28'}
    schedule = requests.get("https://statsapi.web.nhl.com/api/v1/schedule", params=params).json()
    return schedule['dates']
"""

def replace_query_param(url, key, val):
    """
    Given a URL and a key/val pair, set or replace an item in the query
    parameters of the URL, and return the new URL.
    """
    (scheme, netloc, path, query, fragment) = parse.urlsplit(force_str(url))
    query_dict = parse.parse_qs(query, keep_blank_values=True)
    query_dict[force_str(key)] = [force_str(val)]
    query = parse.urlencode(sorted(query_dict.items()), doseq=True)
    return parse.urlunsplit((scheme, netloc, path, query, fragment))


def update_all_games():
    """Get entire schedule available from the API and fill our database with the data.
       Should be an admin task. Nothing user facing should ever interact with this.
    """
    from tripplanner.models import NHLGame, NHLTeam
    params = {'startDate': '2021-02-05', 'endDate': '2021-02-28'}
    schedule = requests.get("https://statsapi.web.nhl.com/api/v1/schedule", params=params).json()
    for games_on_date in schedule['dates']:
        date = games_on_date['date']
        for game in games_on_date['games']:
            home_team, created = NHLTeam.objects.get_or_create(
                                            team_name=game['teams']['home']['team']['name'],
                                            team_id=game['teams']['home']['team']['id'])
            if created:
                home_team.save()
            away_team, created = NHLTeam.objects.get_or_create(
                                            team_name=game['teams']['away']['team']['name'],
                                            team_id=game['teams']['away']['team']['id'])
            if created:
                away_team.save()
            new_game, created = NHLGame.objects.get_or_create(
                                            home_team=home_team,
                                            away_team=away_team,
                                            date=date)
            if created:
                new_game.save()

def get_distance_to_game(starting_country, starting_province, starting_city, team_city):
    """Get distance between 2 cities

    Args:
        starting_country ([type]): The country you are starting in
        starting_province ([type]): The province/state you are starting in
        starting_city ([type]): The city you are starting in
        team_city ([type]): The city that the team is located in

    Returns:
        str: Distance of city to other city in format "123 km"
    """
    API_TOKEN = os.environ.get('MAPS_API_TOKEN')
    if not API_TOKEN:
        sys.exit("Did you forget to set MAPS_API_TOKEN?")
    URL = "https://maps.googleapis.com/maps/api/distancematrix/json?" \
            "origins={origin}&destinations={dest}&key={key}"

    response = requests.get(URL.format(
        origin="{}, {}, {}".format(starting_country, starting_province, starting_city),
        dest=team_city,
        key=API_TOKEN))
    return response.json()['rows'][0]['elements'][0]['distance']['text']  # Yikes
