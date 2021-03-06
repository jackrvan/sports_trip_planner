from django.shortcuts import render

from django_filters.views import FilterView
from django_tables2.views import SingleTableMixin
from django_tables2 import RequestConfig
from tripplanner.filters import NHLGameFilter
from tripplanner.models import NHLGame
from tripplanner.tables import NHLGameTable
from tripplanner.utils import PROVINCES

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
    filterset_class = NHLGameFilter

    def get_table(self, **kwargs):
        table_class = self.get_table_class()
        table = table_class(data=self.get_table_data(), request=self.request, **kwargs)
        return RequestConfig(
            self.request, paginate=self.get_table_pagination(table)
        ).configure(table)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['country'] = self.request.GET.get('country', 'Canada')
        context['province'] = self.request.GET.get('province', 'Canada')
        context['city'] = self.request.GET.get('city', 'Canada')
        return context
