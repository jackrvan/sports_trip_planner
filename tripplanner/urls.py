from django.urls import path

from . import views

app_name = 'tripplanner'

urlpatterns = [
    path('info/<str:team>/<str:start_date>/<str:end_date>', views.GameListView.as_view(), name='info'),
    path('', views.index, name='index'),
]