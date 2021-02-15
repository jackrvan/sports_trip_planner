from typing import ClassVar, Optional

from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView

from tripplanner.forms import NHLForm
from tripplanner.models import NHLGame
from tripplanner.utils import NHL_TEAMS, PROVINCES, get_distance_to_game


def index(request):
    if request.method == 'POST':
        form = NHLForm(request.POST, prefix="nhl_form")
        if form.is_valid():
            print(request.POST)
            team = request.POST['nhl_form-team']
            start_date = request.POST['nhl_form-start_date']
            end_date = request.POST['nhl_form-end_date']
            return HttpResponseRedirect(reverse('tripplanner:info', args=(team, start_date, end_date)))
    else:
        form = NHLForm(prefix="nhl_form", initial={'starting_country': "Canada"})
    return render(request, "tripplanner/index.html", {'form': form})

def load_provinces(request):
    country = request.GET.get('country')
    provinces = PROVINCES[country]
    return render(request, 'tripplanner/province_dropdown_list_options.html', {'provinces': provinces})

class GameListView(ListView):
    model = NHLGame
    template_name = "tripplanner/info_page.html"
    context_object_name = 'games'
    #paginate_by = 50
    _cached_distances: ClassVar[Optional[dict]] = {}


    def get_queryset(self):
        home_team_filter = self.request.GET.get('home_team_filter')
        away_team_filter = self.request.GET.get('away_team_filter')
        date_filter = self.request.GET.get('date_filter')

        games_to_show = NHLGame.objects.all()

        if home_team_filter:
            games_to_show = games_to_show.filter(home_team_name__icontains=home_team_filter)
        if away_team_filter:
            games_to_show = games_to_show.filter(away_team_name__icontains=away_team_filter)
        if date_filter:
            games_to_show = games_to_show.filter(date__icontains=date_filter)
        return games_to_show

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['home_team_filter_initial'] = self.request.GET.get('home_team_filter', '')
        context['away_team_filter_initial'] = self.request.GET.get('away_team_filter', '')
        context['date_filter_initial'] = self.request.GET.get('date_filter', '')
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
                                               team) for team in NHL_TEAMS
                }
            context['distances'] = GameListView._cached_distances[city]
        else:
            context['distances'] = {
                team: "Unknown" for team in NHL_TEAMS
            }
        return context
