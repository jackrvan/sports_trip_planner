from django import forms

from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, Submit
from tripplanner.utils import NHL_TEAMS, PROVINCES


class NHLForm(forms.Form):
    starting_country = forms.ChoiceField(choices=[("Canada", "Canada"), ("USA", "USA")])
    starting_province = forms.ChoiceField(choices=[(x, x) for x in PROVINCES["Canada"]])
    starting_city = forms.CharField()

    helper = FormHelper()
    helper.layout = Layout(
        Field('starting_country', css_class="form-control"),
        Field('starting_province', css_class="form-control"),
        Field('starting_city', css_class="form-control"),
    )
    helper.form_class = 'form-horizontal'

    helper.use_custom_control = False
    helper.label_class = 'col-4'
    helper.field_class = 'col-8'
    helper.form_tag = False
