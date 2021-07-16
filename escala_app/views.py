from django.http import request
from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from escala_app.models import Medicos, Postos, Dia_de_Folga, Escala
from escala_app.forms import MedicosForm, PostosForm, Dia_de_FolgaForm, EscalaForm
from django.views.generic import (CreateView,UpdateView, 
                                        ListView,DetailView,DeleteView)

# Create your views here.
def index(request):
    return render(request, 'escala_app/index.html')

class MedicosListView(ListView):
    context_object_name = 'item_list'
    extra_context={'name': 'Médicos'}
    model = Medicos
    template_name = 'escala_app/list.html'
    def get_ordering(self):
        ordering = self.request.GET.get('ordering', 'nome')
        # validate ordering here
        return ordering

class MedicosDetailView(DetailView):
    model = Medicos
    context_object_name = 'medicos_detail'
    template_name = 'escala_app/medicos_detail.html'
    
class MedicosCreateView(CreateView):

    def get(self, request, *args, **kwargs):
        context = {'form': MedicosForm(), 'name': 'Médicos'}
        return render(request, 'escala_app/form.html', context)

    def post(self, request, *args, **kwargs):
        form = MedicosForm(request.POST)
        if form.is_valid():
            medico = form.save()
            medico.save()
            return HttpResponseRedirect(reverse_lazy('escala_app:medicoslist'))
        return render(request, 'escala_app/form.html', {'form': form})


class MedicosUpdateView(UpdateView):
    model = Medicos
    fields = ['nome', 'sobrenome', 'data_admissao', 'status']
    template_name = 'escala_app/form.html'

class MedicosDeleteView(DeleteView):
    model = Medicos
    success_url = reverse_lazy("escala_app:medicos")

class PostosCreateView(CreateView):

    def get(self, request, *args, **kwargs):
        context = {'form': PostosForm(), 'name': 'Postos'}
        return render(request, 'escala_app/form.html', context)

    def post(self, request, *args, **kwargs):
        form = PostosForm(request.POST)
        if form.is_valid():
            posto = form.save()
            posto.save()
            return HttpResponseRedirect(reverse_lazy('escala_app:postoslist'))
        return render(request, 'escala_app/form.html', {'form': form})

class PostosListView(ListView):
    model = Postos
    extra_context={'name': 'Postos'}
    context_object_name = 'item_list'
    template_name = 'escala_app/list.html'

class PostosDetailView(DetailView):
    model = Postos
    context_object_name = 'postos_detail'
    template_name = 'escala_app/postos_detail.html'

class PostosUpdateView(UpdateView):
    model = Postos
    fields = ['nome', 'endereco', 'status']
    template_name = 'escala_app/form.html'


class FolgaCreateView(CreateView):

    def get(self, request, *args, **kwargs):
        context = {'form': Dia_de_FolgaForm(), 'name': 'dias de folga'}
        return render(request, 'escala_app/form.html', context)

    def post(self, request, *args, **kwargs):
        form = Dia_de_FolgaForm(request.POST)
        if form.is_valid():
            df = form.save()
            df.save()
            return HttpResponseRedirect(reverse_lazy('escala_app:folgalist'))
        return render(request, 'escala_app/form.html', {'form': form})


class FolgaListView(ListView):
    model = Dia_de_Folga
    extra_context={'name': 'dias de folga'}
    context_object_name = 'item_list'
    template_name = 'escala_app/list.html'
    def get_ordering(self):
        ordering = self.request.GET.get('ordering', 'dia_folga')
        # validate ordering here
        return ordering

class FolgaUpdateView(UpdateView):
    model = Dia_de_Folga
    form_class = Dia_de_FolgaForm
    template_name = 'escala_app/form.html'

class FolgaDeleteView(DeleteView):
    model = Dia_de_Folga
    extra_context={'name': 'Folga'}
    context_object_name = 'item'
    success_url = reverse_lazy("escala_app:folgalist")

class EscalaCreateView(CreateView):

    def get(self, request, *args, **kwargs):
        context = {'form': EscalaForm(), 'name': 'escala'}
        return render(request, 'escala_app/form.html', context)

    def post(self, request, *args, **kwargs):
        form = EscalaForm(request.POST)
        if form.is_valid():
            escala = form.save()
            escala.save()
            return HttpResponseRedirect(reverse_lazy('escala_app:escalalist'))
        return render(request, 'escala_app/form.html', {'form': form})

class EscalaListView(ListView):
    context_object_name = 'item_list'
    extra_context={'name': 'Escala'}
    model = Escala
    template_name = 'escala_app/list.html'
    def get_ordering(self):
        ordering = self.request.GET.get('ordering', 'data')
        # validate ordering here
        return ordering

class EscalaUpdateView(UpdateView):
    model = Escala
    form_class = EscalaForm
    template_name = 'escala_app/form.html'

class EscalaDeleteView(DeleteView):
    model = Escala
    template_name = 'escala_app/dia_de_folga_confirm_delete.html'
    extra_context={'name': 'Escala'}
    context_object_name = 'item'
    success_url = reverse_lazy("escala_app:escalalist")