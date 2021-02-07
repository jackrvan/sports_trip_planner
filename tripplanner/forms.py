from django import forms
from django.forms.widgets import SelectDateWidget

from tripplanner.utils import NHL_TEAMS


class NHLForm(forms.Form):
    team = forms.ChoiceField(choices=[(x, x) for x in NHL_TEAMS])
    start_date = forms.DateField(widget=SelectDateWidget())
    end_date = forms.DateField(widget=SelectDateWidget())
