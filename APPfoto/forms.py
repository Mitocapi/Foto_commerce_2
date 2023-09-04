from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from .models import *

from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class SearchForm(forms.Form):
    CHOICE_LIST = [
        ("name", "Cerca nome foto"),
        ("artist_name", "Cerca nome fotografo"),
        ("main_colour", "Cerca per colore principale"),
        ("Orientamento", "Cerca per orientamento")
    ]

    COLOUR_CHOICES = ["Black", "Dark Blue", "Green", "Gray", "Light Blue", "Orange", "Pink",
                      "Purple", "Red", "White", "Yellow"]

    helper = FormHelper()
    helper.form_id = 'search_crispy_form'
    helper.form_method = "POST"
    helper.add_input(Submit('submit', 'Cerca'))

    search_string = forms.CharField(label="Cerca qualcosa", max_length=100, min_length=1, required=True)
    search_where = forms.ChoiceField(label="Ricerca per: ", required=True, choices=CHOICE_LIST)



class FotoCrispyForm(forms.ModelForm):

    helper = FormHelper()
    helper.form_id = 'foto-crispy-form'
    helper.form_method = 'POST'
    helper.add_input(Submit('submit','Submit'))

    class Meta:
        model = Foto
        fields = ('name', 'artist', 'main_colour', 'landscape')


class CreateFotoForm(forms.ModelForm):
    helper = FormHelper()
    helper.form_id = "addfoto_crispy_form"
    helper.form_method = "POST"
    helper.add_input(Submit("submit", "Aggiungi Foto"))


    class Meta:
        model = Foto
        fields = ["name", "main_colour", "landscape", "actual_photo" ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["artist"].widget.attrs["readonly"] = True


class AcquistoForm(forms.ModelForm):
    class Meta:
        model = Acquisto
        fields = ["foto", "acquirente", "materiale", "dimensioni"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["acquirente"].disabled = True
        self.fields["foto"].disabled = True
        self.helper = FormHelper()
        self.helper.form_id = "acquisto_crispy_form"
        self.helper.form_method = "POST"
        self.helper.add_input(Submit("submit", "Completa l'acquisto"))