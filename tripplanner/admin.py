import requests
from django.contrib import admin

from tripplanner.models import NHLGame, NHLTeam
from tripplanner.utils import update_all_games


@admin.register(NHLGame)
class NHLGamesAdmin(admin.ModelAdmin):
    actions = ['get_nhl_games']

    def get_nhl_games(self, request, queryset):
        print("Updating all NHL games")
        update_all_games()
        self.message_user(request, 'Added new games')

@admin.register(NHLTeam)
class NHLTeamsAdmin(admin.ModelAdmin):
    actions = ['get_nhl_teams']

    def get_nhl_teams(self, request, queryset):
        URL = "https://statsapi.web.nhl.com/api/v1/teams"
        response = requests.get(URL).json()
        for team in response['teams']:
            new_team, created = NHLTeam.objects.get_or_create(team_name=team['name'],
                                                              team_id=team['id'],
                                                              city=team['venue']['city'])
            if created:
                new_team.save()
        self.message_user(request, "Added NHL Teams")
