from django.urls import path

from . import views

app_name = 'tripplanner'

urlpatterns = [
    path('ajax/load-cities/', views.load_provinces, name='ajax_load_provinces'),
    path('', views.GameListView.as_view(), name='index'),
]
