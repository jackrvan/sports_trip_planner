from django.contrib import admin
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME

from .models import NHLGame
from .utils import update_all_games

# Register your models here.
#admin.site.register(NHLGame)

@admin.register(NHLGame)
class NHLGamesAdmin(admin.ModelAdmin):
    actions = ['get_nhl_games']

    def get_nhl_games(self, request, queryset):
        print("Updating all NHL games")
        update_all_games()
        self.message_user(request, 'Added new games')