import requests

from tripplanner.models import NHLGame

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

NHL_TEAMS = [
    'Anaheim Ducks',
    'Arizona Coyotes',
    'Boston Bruins',
    'Buffalo Sabres',
    'Calgary Flames',
    'Carolina Hurricanes',
    'Chicago Blackhawks',
    'Colorado Avalanche',
    'Columbus Blue Jackets',
    'Dallas Stars',
    'Detroit Red Wings',
    'Edmonton Oilers',
    'Florida Panthers',
    'Los Angeles Kings',
    'Minnesota Wild',
    'Montréal Canadiens',
    'Nashville Predators',
    'New Jersey Devils',
    'New York Islanders',
    'New York Rangers',
    'Ottawa Senators',
    'Philadelphia Flyers',
    'Pittsburgh Penguins',
    'San Jose Sharks',
    'St. Louis Blues',
    'Tampa Bay Lightning',
    'Toronto Maple Leafs',
    'Vancouver Canucks',
    'Vegas Golden Knights',
    'Washington Capitals',
    'Winnipeg Jets',
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

def get_games(team_name):
    all_teams = requests.get("https://statsapi.web.nhl.com/api/v1/teams").json()
    team_id = next(team['id'] for team in all_teams['teams'] if team['name'] == team_name)
    params = {'teamId': team_id, 'startDate': '2021-02-05', 'endDate': '2021-02-28'}
    schedule = requests.get("https://statsapi.web.nhl.com/api/v1/schedule", params=params).json()
    return schedule['dates']

def update_all_games():
    params = {'startDate': '2021-02-05', 'endDate': '2021-02-28'}
    schedule = requests.get("https://statsapi.web.nhl.com/api/v1/schedule", params=params).json()
    for games_on_date in schedule['dates']:
        date = games_on_date['date']
        for game in games_on_date['games']:
            home_team = game['teams']['home']['team']
            away_team = game['teams']['away']['team']
            new_game, created = NHLGame.objects.get_or_create(home_team_name=home_team['name'],
                                                              home_team_id=home_team['id'],
                                                              away_team_name=away_team['name'],
                                                              away_team_id=away_team['id'],
                                                              date=date)
            if created:
                new_game.save()

def get_distance_to_game(starting_country, starting_province, starting_city, team_city):
    API_TOKEN = "AIzaSyD575w7qNL09i9qqaamBxO8qIDCQKYzqdE"
    URL = "https://maps.googleapis.com/maps/api/distancematrix/json?origins={origin}&destinations={dest}&key={key}"

    response = requests.get(URL.format(
        origin="{}, {}, {}".format(starting_country, starting_province, starting_city),
        dest=team_city,
        key=API_TOKEN))
    return response.json()['rows'][0]['elements'][0]['distance']['text']  # Yikes
