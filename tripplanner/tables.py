from django.db.models import Min, Q
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
                distance = distance_object.values()[0]['distance']

            return distance
        return "Unknown"

    def order_distance(self, queryset, is_descending):
        """Order by our custom distance column
        """
        country = self.request.GET.get('country', '')
        province = self.request.GET.get('province', '')
        city = self.request.GET.get('city', '')
        for team in NHLTeam.objects.all():
            # We need to loop through and make sure we have all the distances in the db first
            distance_object = Distance.objects.filter(starting_country=country,
                                                      starting_province=province,
                                                      starting_city=city,
                                                      destination=team)
            if distance_object:
                assert len(distance_object) == 1, \
                    f"Howd you get more than one distance between {city} and {team}"
            else:
                distance = get_distance_to_game(starting_country=country,
                                                starting_province=province,
                                                starting_city=city,
                                                team_city=team.city)[:-3].replace(',', '')
                distance_object = Distance(starting_country=country,
                                           starting_province=province,
                                           starting_city=city,
                                           destination=team,
                                           distance=distance)
                distance_object.save()
        my_filter = Min('home_team__distance__distance',
                        filter=(Q(home_team__distance__starting_country=country) &
                                Q(home_team__distance__starting_province=province) &
                                Q(home_team__distance__starting_city=city)))
        print("with filter = {}".format(queryset.aggregate(thing=my_filter)))
        sorted_queryset = queryset.annotate(distances=my_filter).order_by(
            "distances" if not is_descending else "-distances")
        print(f"sorted= {sorted_queryset}")
        return (sorted_queryset, True)
