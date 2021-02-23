from typing import ClassVar, Optional

from django.shortcuts import render

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from tripplanner.filters import NHLGameFilter
from tripplanner.models import NHLGame, NHLTeam
from tripplanner.tables import NHLGameTable
from tripplanner.utils import PROVINCES, get_distance_to_game
from django_tables2 import RequestConfig 

def load_provinces(request):
    """When the user changes the country we want to change the province dropdown

    Args:
        request (WSGIRequest): Request object

    Returns:
        Rendered html of the new dropdown options
    """
    country = request.GET.get('country')
    provinces = PROVINCES[country]
    return render(request, 'tripplanner/province_dropdown_list_options.html', {'provinces': provinces})

class GameListView(SingleTableMixin, FilterView):
    model = NHLGame
    template_name = "tripplanner/index.html"
    context_object_name = 'games'
    paginate_by = 25
    table_class = NHLGameTable
    _cached_distances: ClassVar[Optional[dict]] = {}
    filterset_class = NHLGameFilter

    def get_table(self, **kwargs):
        table_class = self.get_table_class()
        table = table_class(data=self.get_table_data(), request=self.request, **kwargs)
        return RequestConfig(
            self.request, paginate=self.get_table_pagination(table)
        ).configure(table)

    """
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        country = self.request.GET.get('country', '')
        province = self.request.GET.get('province', '')
        city = self.request.GET.get('city', '')
        if city:
            print("CACHE = {}".format(GameListView._cached_distances))
            if city not in GameListView._cached_distances:
                GameListView._cached_distances[city] = {
                    team: get_distance_to_game(country, province, city,
                                               team) for team in [x.team_name for x in NHLTeam.objects.all()]
                }
            context['distances'] = GameListView._cached_distances[city]
        else:
            context['distances'] = {
                team: "Unknown" for team in [x.team_name for x in NHLTeam.objects.all()]
            }
        return context

    
    def get_queryset(self):
        home_team_filter = self.request.GET.get('home_team_filter')
        away_team_filter = self.request.GET.get('away_team_filter')
        date_filter_begin = self.request.GET.get('date_filter_begin') or '01-01-21'
        date_filter_end = self.request.GET.get('date_filter_end') or '31-12-21'

        # Need to reverse the dates and append 20 since format on page is dd-mm-yy but django likes yyyy-mm-dd
        date_filter_begin = '20{}-{}-{}'.format(date_filter_begin.split('-')[2],
                                                date_filter_begin.split('-')[1],
                                                date_filter_begin.split('-')[0])
        date_filter_end = '20{}-{}-{}'.format(date_filter_end.split('-')[2],
                                              date_filter_end.split('-')[1],
                                              date_filter_end.split('-')[0])

        games_to_show = NHLGame.objects.all()

        if home_team_filter:
            games_to_show = games_to_show.filter(home_team__team_name__icontains=home_team_filter)
        if away_team_filter:
            games_to_show = games_to_show.filter(away_team__team_name__icontains=away_team_filter)
        games_to_show = games_to_show.filter(date__range=[date_filter_begin, date_filter_end])
        return games_to_show

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['home_team_filter_initial'] = self.request.GET.get('home_team_filter', '')
        context['away_team_filter_initial'] = self.request.GET.get('away_team_filter', '')
        context['date_filter_begin_initial'] = self.request.GET.get('date_filter_begin', '')
        context['date_filter_end_initial'] = self.request.GET.get('date_filter_end', '')
        context['starting_country_initial'] = self.request.GET.get('nhl_form-starting_country', 'Canada')
        context['starting_province_initial'] = self.request.GET.get('nhl_form-starting_province', '')
        context['starting_city_initial'] = self.request.GET.get('nhl_form-starting_city', '')
        city = self.request.GET.get('nhl_form-starting_city', None)
        context['provinces'] = {
            province: False for province in PROVINCES[context['starting_country_initial']]
        }
        context['provinces'][context['starting_province_initial']] = True
        if city:
            print("CACHE = {}".format(GameListView._cached_distances))
            if city not in GameListView._cached_distances:
                GameListView._cached_distances[city] = {
                    team: get_distance_to_game(self.request.GET.get('nhl_form-starting_country', ''),
                                               self.request.GET.get('nhl_form-starting_province', ''),
                                               city,
                                               team) for team in [x.team_name for x in NHLTeam.objects.all()]
                }
            context['distances'] = GameListView._cached_distances[city]
        else:
            context['distances'] = {
                team: "Unknown" for team in [x.team_name for x in NHLTeam.objects.all()]
            }
        return context
"""