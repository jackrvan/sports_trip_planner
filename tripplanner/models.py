from django.db import models

# Create your models here.
class NFLTicket(models.Model):
    price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True)
    home_team = models.CharField(max_length=50)
    away_team = models.CharField(max_length=50)
    date = models.DateTimeField()
    section = models.CharField(max_length=5)  # What are the chances a section is > 5 chars
    seat = models.CharField(max_length=3)

class NHLGame(models.Model):
    home_team_name = models.CharField(max_length=50)
    home_team_id = models.IntegerField()
    away_team_name = models.CharField(max_length=50)
    away_team_id = models.IntegerField()
    date = models.DateField()

    def __str__(self):
        return "{}: {} @ {}".format(self.date, self.away_team_name, self.home_team_name)
