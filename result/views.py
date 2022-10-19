from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, ListView, DeleteView

from .models import Result, Token
from .forms import CreateResultForm
# Create your views here.


def index(request):
    return render(request, 'index.html', {})


class CreateResultView(CreateView):
    model = Result
    form_class = CreateResultForm
    template_name = 'result_create.html'

    def get_success_url(self):
        return reverse('index')


class UpdateResultView(UpdateView):
    model = Result
    form_class = CreateResultForm
    template_name = 'result_edit_delete.html'

    def get_success_url(self):
        return reverse('index')


def delete_result_view(request, *args, **kwargs):
    result = Result.objects.get_object_or_404(pk=kwargs['pk'])
    if result.is_inactive:
        result.is_inactive = False
    else:
        result.is_inactive = True
    return render(request, 'result_edit_delete.html', {})


class AllResultView(ListView):
    model = Result
    template_name = 'result_list.html'

    def get_queryset(self):
        return Result.objects.all()


