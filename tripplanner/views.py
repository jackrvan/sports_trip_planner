from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.generic.list import ListView

from tripplanner.forms import NHLForm
from tripplanner.models import NHLGame
from tripplanner.utils import NHL_TEAMS


# Create your views here.',
def index(request):
    #context = {'NHL_TEAMS': NHL_TEAMS}
    if request.method == 'POST':
        form = NHLForm(request.POST)
        if form.is_valid():
            team = request.POST['team']
            print(request.POST)
            start_date = '{}-{}-{}'.format(request.POST['start_date_year'],
                                           request.POST['start_date_month'],
                                           request.POST['start_date_day'])
            end_date = '{}-{}-{}'.format(request.POST['end_date_year'],
                                         request.POST['end_date_month'],
                                         request.POST['end_date_day'])
            return HttpResponseRedirect(reverse('tripplanner:info', args=(team, start_date, end_date)))
    else:
        form = NHLForm()
    return render(request, "tripplanner/index.html", {'form': form})

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
