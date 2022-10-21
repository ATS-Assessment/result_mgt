from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import CreateView, UpdateView

from .models import Result, Token
from .forms import CreateResultForm
# Create your views here.


def index(request):
    return render(request, 'index.html', {})


class CreateResultView(CreateView):
    model = Result
    form_class = CreateResultForm
    template_name = 'result_create.html'
    success_url = 'dashboard'



