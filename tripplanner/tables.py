import django_tables2 as tables
from tripplanner.models import Distance, NHLGame, NHLTeam
from tripplanner.utils import get_distance_to_game


class NHLGameTable(tables.Table):
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
        country = self.request.GET.get('country', '')
        province = self.request.GET.get('province', '')
        city = self.request.GET.get('city', '')
        if city:
            team_object = NHLTeam.objects.filter(team_name=record.home_team)
            assert len(team_object) == 1
            # Check to see if we already have this Distance in our database
            distance_object = Distance.objects.filter(destination=team_object[0],
                                                      starting_country=country,
                                                      starting_province=province,
                                                      starting_city=city)
            assert len(distance_object) == 1 or len(distance_object) == 0, \
                "Howd you end up with more than one distance from {} to {}".format(team_object[0],
                                                                                   city)
            if not distance_object:
                print("Making new entry for {} to {}".format(city, team_object[0]))
                # Get distance to game and strip ending " km" and delete commas
                distance = get_distance_to_game(starting_country=country,
                                                starting_province=province,
                                                starting_city=city,
                                                team_city=str(team_object[0]))[:-3].replace(',', '')
                # We dont have it in the db so add it
                distance_object = Distance(destination=team_object[0],
                                           starting_country=country,
                                           starting_province=province,
                                           starting_city=city,
                                           distance=distance)
                distance_object.save()
            else:
                print("using cache for {} to {}".format(city, team_object[0]))
                distance = distance_object.values()[0]['distance']

            print("Distance object = {}".format(distance_object))
            return distance
        return "Unknown"

    def order_distance(self, queryset, is_descending):
        """Order by our custom distance column
        """
        all_teams = [x.home_team.team_name for x in queryset]
        for team in all_teams:
            pass
        print("All teams = {}".format(all_teams))
        return (queryset, True)
