import requests

from tripplanner.models import NHLGame, NHLTeam

NFL_TEAMS = [
    'Arizona Cardinals',
    'Atlanta Falcons',
    'Baltimore Ravens',
    'Buffalo Bills',
    'Carolina Panthers',
    'Chicago Bears',
    'Cincinnati Bengals',
    'Cleveland Browns',
    'Dallas Cowboys',
    'Denver Broncos',
    'Detroit Lions',
    'Green Bay Packers',
    'Houston Texans',
    'Indianapolis Colts',
    'Jacksonville Jaguars',
    'Kansas City Chiefs',
    'Las Vegas Raiders',
    'Los Angeles Chargers',
    'Los Angeles Rams',
    'Miami Dolphins',
    'Minnesota Vikings',
    'New England Patriots',
    'New Orleans Saints',
    'New York Giants',
    'New York Jets',
    'Philadelphia Eagles',
    'Pittsburgh Steelers',
    'San Francisco 49ers',
    'Seattle Seahawks',
    'Tampa Bay Buccaneers',
    'Tennessee Titans',
    'Washington Football Team',
]

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


def update_all_games():
    """Get entire schedule available from the API and fill our database with the data.
       Should be an admin task. Nothing user facing should ever interact with this. 
    """
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
    API_TOKEN = "AIzaSyD575w7qNL09i9qqaamBxO8qIDCQKYzqdE"
    URL = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={dest}&key={key}"

    response = requests.get(URL.format(
        origin="{}, {}, {}".format(starting_country, starting_province, starting_city),
        dest=team_city,
        key=API_TOKEN))
    return response.json()['rows'][0]['elements'][0]['distance']['text']  # Yikes
