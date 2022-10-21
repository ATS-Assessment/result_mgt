from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView,\
    ListView, DeleteView, DetailView

from .models import Result, Token
from .forms import CreateResultForm
# Create your views here.


def index(request):
    return render(request, 'index.html', {})


# class CreateResultView(CreateView):
#     model = Result
#     form_class = CreateResultForm
#     template_name = 'result_create.html'

#     def get_success_url(self):
#         return reverse('index')


class ResultDetailView(DetailView):
    model = Result
    template_name = 'result_detail.html'


def delete_result_view(request, pk, *args, **kwargs):
    pass


class UpdateResultView(UpdateView):
    model = Result
    form_class = CreateResultForm

    def get_success_url(self):
        return reverse('index')
    template_name = 'result_create.html'
    success_url = 'dashboard'


class AllResultView(ListView):
    model = Result
    template_name = 'result_list.html'
    context_object_name = 'results'

    def get_queryset(self):
        return Result.objects.all()


class AllResultsByClass(ListView):
    model = Result
    template_name = 'result_list.html'
    context_object_name = 'results_by_class'

    def get_queryset(self):
        pass
