from django.db import models
from django.utils import timezone

from tripplanner.utils import COUNTRY_CHOICES


class NHLTeam(models.Model):
    team_name = models.CharField(max_length=50)
    team_id = models.IntegerField()  # The NHL API gives each team an id. Probably useful to save it.
    city = models.CharField(max_length=50)

    def __str__(self):
        return '{}'.format(self.team_name)


class NHLGame(models.Model):
    home_team = models.ForeignKey(NHLTeam, on_delete=models.CASCADE, related_name="home_team")
    away_team = models.ForeignKey(NHLTeam, on_delete=models.CASCADE, related_name="away_team")
    date = models.DateField()

    def __str__(self):
        return "{}: {} @ {}".format(self.date, self.away_team, self.home_team)

    def is_in_future(self):
        """Returns True if the game is in the future and hasnt already been played
        """
        return self.date >= timezone.now()

class Distance(models.Model):
    destination = models.ForeignKey(NHLTeam, on_delete=models.CASCADE)
    starting_country = models.CharField(max_length=2,
                                        choices=COUNTRY_CHOICES)
    starting_province = models.CharField(max_length=50)
    starting_city = models.CharField(max_length=50)
    distance = models.DecimalField(decimal_places=1, max_digits=6)

    def __str__(self):
        return 'Travelling from {} to {}'.format(self.starting_city, self.destination)
