import datetime

from django.test import TestCase
from django.utils import timezone

from tripplanner.models import NHLGame, NHLTeam


class NHLGameModelTests(TestCase):
    def setUp(self):
        NHLTeam.objects.create(team_name="homeTeamName",
                               team_id=1,
                               city='cityName')
        NHLTeam.objects.create(team_name="awayTeamName",
                               team_id=2,
                               city='cityName2')

    def test_str(self):
        home_team = NHLTeam.objects.get(team_id=1)
        away_team = NHLTeam.objects.get(team_id=2)
        nhl_game = NHLGame(home_team=home_team,
                           away_team=away_team,
                           date='2021-02-15')
        self.assertEqual(str(nhl_game),
                         "2021-02-15: awayTeamName @ homeTeamName")

    def test_is_in_future_with_future_game(self):
        """Test the is_in_future method when the game is in the future
        """
        home_team = NHLTeam.objects.get(team_id=1)
        away_team = NHLTeam.objects.get(team_id=2)
        nhl_game = NHLGame(home_team=home_team,
                           away_team=away_team,
                           date=timezone.now() + datetime.timedelta(days=1, seconds=1))
        self.assertTrue(nhl_game.is_in_future())

    def test_is_in_future_with_past_game(self):
        """Test the is_in_future method when the game is in the past
        """
        home_team = NHLTeam.objects.get(team_id=1)
        away_team = NHLTeam.objects.get(team_id=2)
        nhl_game = NHLGame.objects.create(home_team=home_team,
                           away_team=away_team,
                           date=timezone.now() - datetime.timedelta(days=1, seconds=1))
        self.assertFalse(nhl_game.is_in_future())
