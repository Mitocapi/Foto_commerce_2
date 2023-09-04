from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
# Create your views here.


def home_view(request):
    return render(request, template_name="APPfotoTempl/home.html")


from .forms import SearchForm  # Import your form class

from django.shortcuts import render
from django.views import View




class SearchWrongColourView(View):
    template_name = "APPfotoTempl/search_wrong_colour.html"

    def get(self, request, *args, **kwargs):
        form = SearchForm()  # Replace with your actual form class
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        if request.method == "POST":
            form = SearchForm(request.POST)
            if form.is_valid():
                sstring = form.cleaned_data.get("search_string")
                where = form.cleaned_data.get("search_where")
                return redirect("APPfoto:ricerca_risultati", sstring, where)
            else:
                context = {'form': form}
            return render(request, self.template_name, context)


class FotoListView(ListView):
    titolo="Abbiamo trovato queste foto"
    model = Foto
    template_name = "APPfotoTempl/lista_foto.html"

def search(request):
    if request.method == "POST":
        form = SearchForm(request.POST)
        if form.is_valid():
            sstring = form.cleaned_data.get("search_string")
            where = form.cleaned_data.get("search_where")
            return redirect("APPfoto:ricerca_risultati", sstring, where)

    else:
        form = SearchForm()

    return render(request, "APPfotoTempl/search.html", context= {"form": form})


class FotoListaRicercataView(FotoListView):
    titolo = "risultati ricerca"

    paginate_by = 10

    def get_queryset(self):
        sstring = self.kwargs['sstring']
        where = self.kwargs['where']


        if where == "name":
            qq = self.model.objects.filter(name__icontains=sstring)
        elif where == "landscape":
            # Filter using a boolean condition
            qq = self.model.objects.filter(landscape=True)
        elif where == "main_colour":
            # Filter using elements from a list
            COLOUR_CHOICES_to_filter = ["Black","Dark Blue","Green", "Gray", "Light Blue", "Orange", "Pink",
                                        "Purple", "Red", "White", "Yellow"]
            qq = self.model.objects.filter(main_colour__in=sstring)
        else:
            qq = self.model.objects.filter(artist__username__icontains=sstring)

        return qq



# views.py
class CreateFotoView(LoginRequiredMixin, CreateView):
    model = Foto
    fields = ['name', 'main_colour', 'landscape', 'actual_photo']
    template_name = 'APPfotoTempl/create_entry.html'
    success_url = reverse_lazy("APPfoto:home")

    def form_valid(self, form):
        form.instance.artist = self.request.user
        return super().form_valid(form)


@login_required
def my_situation(request):
     user = get_object_or_404(User, pk=request.user.pk)
     return render(request, "APPfotoTempl/situation.html")



@login_required
def CreaAcquisto(request, foto_id):
    foto = Foto.objects.get(pk=foto_id)

    if request.method == "POST":
        form = AcquistoForm(request.POST, initial={'foto': foto, 'acquirente': request.user})

        if form.is_valid():
            acquisto = form.save(commit=False)
            acquisto.foto = foto
            acquisto.acquirente = request.user
            acquisto.save()
            return redirect('APPfoto:situation')
        else:
            messages.error(request, "Invalid form data. Please correct the errors.")
    else:
        initial_data = {'foto': foto, 'acquirente': request.user}
        form = AcquistoForm(initial=initial_data)

    # Make the acquirente field readonly and disabled
    form.fields['acquirente'].widget.attrs['readonly'] = True
    form.fields['acquirente'].widget.attrs['disabled'] = True

    context = {
        'foto': foto,
        'form': form,
    }

    return render(request, 'APPfotoTempl/acquisto.html', context)


