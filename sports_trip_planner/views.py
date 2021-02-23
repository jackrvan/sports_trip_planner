# Create your views here.
from django.shortcuts import redirect, render
from django.urls import reverse

from tripplanner.utils import PROVINCES


def index(request):
    if request.method == "POST":
        return redirect('{}?country={}&province={}&city={}'.format(reverse('tripplanner:index'),
                                                                   request.POST['nhl_form-starting_country'],
                                                                   request.POST['nhl_form-starting_province'],
                                                                   request.POST['nhl_form-starting_city']))
    provinces = PROVINCES["Canada"]  # To start
    return render(request, 'index.html', {'provinces': provinces})

def about(request):
    return render(request, 'about.html')
