import datetime

from django.test import TestCase
from django.urls import reverse
from django.utils import dateformat, timezone

from tripplanner.models import NHLGame, NHLTeam


# MODEL TESTS
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

class NHLTeamModelTests(TestCase):
    def test_str(self):
        team = NHLTeam(team_name="teamName", team_id=1, city='city')
        self.assertEqual(str(team), "teamName")


# VIEW TESTS
class GameListViewTests(TestCase):
    def setUp(self):
        NHLTeam.objects.create(team_name="homeTeamName",
                               team_id=1,
                               city='cityName')
        NHLTeam.objects.create(team_name="awayTeamName",
                               team_id=2,
                               city='cityName2')

    def test_no_games(self):
        response = self.client.get(reverse('tripplanner:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No games were found")
        self.assertQuerysetEqual(response.context['games'], [])

    def test_two_games(self):
        home_team = NHLTeam.objects.get(team_id=1)
        away_team = NHLTeam.objects.get(team_id=2)
        NHLGame.objects.create(home_team=home_team,
                               away_team=away_team,
                               date=timezone.now())
        NHLGame.objects.create(home_team=home_team,
                               away_team=away_team,
                               date=timezone.now() + datetime.timedelta(days=1, seconds=1))
        response = self.client.get(reverse('tripplanner:index'))
        today = dateformat.format(timezone.localtime(timezone.now()), 'Y-m-d')
        tomorrow = dateformat.format(timezone.localtime(timezone.now())+
                                        datetime.timedelta(days=1, seconds=1), 'Y-m-d')
        expected = ['<NHLGame: {}: awayTeamName @ homeTeamName>'.format(today),
                    '<NHLGame: {}: awayTeamName @ homeTeamName>'.format(tomorrow)]
        self.assertQuerysetEqual(response.context['games'], expected, ordered=False)
