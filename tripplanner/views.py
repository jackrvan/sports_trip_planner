from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView

from tripplanner.forms import NHLForm
from tripplanner.models import NHLGame
from tripplanner.utils import PROVINCES


# Create your views here.',
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

    def get_queryset(self):
        return NHLGame.objects.filter((Q(home_team_name=self.kwargs['team']) |
                                        Q(away_team_name=self.kwargs['team'])) &
                                        Q(date__range=[self.kwargs['start_date'], self.kwargs['end_date']]))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['team'] = self.kwargs['team']
        context['start_date'] = self.kwargs['start_date']
        context['end_date'] = self.kwargs['end_date']
        return context
