from typing import ClassVar, Optional

import django_tables2 as tables
from tripplanner.models import NHLGame
from tripplanner.utils import get_distance_to_game


class NHLGameTable(tables.Table):
    _cached_distances: ClassVar[Optional[dict]] = {}
    distance = tables.Column(empty_values=())
    class Meta:
        model = NHLGame
        template_name = "django_tables2/bootstrap4.html"
        fields = ('home_team', 'away_team', 'date', 'distance')

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request")
        super().__init__(*args, **kwargs)

    def order_home_team(self, queryset, is_descending):
        """Custom function to sort the home team since its a foreign key.

        Args:
            queryset (QuerySet): QuerySet of objects
            is_descending (bool): Are we sorting descending?

        Returns:
            (QuerySet, bool): New sorted queryset, do we want to use new queryset?
        """
        queryset = queryset.order_by(('-' if is_descending else '') + "home_team__team_name")
        return (queryset, True)

    def order_away_team(self, queryset, is_descending):
        """Custom function to sort the away team since its a foreign key.

        Args:
            queryset (QuerySet): QuerySet of objects
            is_descending (bool): Are we sorting descending?

        Returns:
            (QuerySet, bool): New sorted queryset, do we want to use new queryset?
        """
        queryset = queryset.order_by(('-' if is_descending else '') + "away_team__team_name")
        return (queryset, True)


    def render_distance(self, record):
        """Render our custom distance column
        """
        country = self.request.GET['country']
        province = self.request.GET['province']
        city = self.request.GET['city']
        if record.home_team not in NHLGameTable._cached_distances:
            NHLGameTable._cached_distances[record.home_team] = get_distance_to_game(
                starting_country=country,
                starting_province=province,
                starting_city=city,
                team_city=record.home_team)
        return NHLGameTable._cached_distances[record.home_team]
