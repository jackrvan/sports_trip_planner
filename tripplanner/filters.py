import django_filters
from tripplanner.models import NHLGame


class NHLGameFilter(django_filters.FilterSet):
    date = django_filters.DateFromToRangeFilter()
    class Meta:
        model = NHLGame
        fields = {
            'home_team__team_name': ['icontains'],
            'away_team__team_name': ['icontains'],
            'date': [],
        }
