from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView,\
    ListView, DeleteView, DetailView, View

from .models import Result, Score, Token
from klass.models import Subject
from django.contrib import messages
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


class ResultDetailView(View):
    model = Result
    template_name = 'klass/result_details.html'

    def get(self, request, pk):
        result = Result.objects.get(pk=pk)
        context = {
            "results": Score.objects.filter(result__pk=pk),
            "info": result
        }
        return render(request, self.template_name, context)


def delete_result_view(request, pk, *args, **kwargs):
    pass


class UpdateResultView(UpdateView):
    model = Result
    form_class = CreateResultForm

    def get_success_url(self):
        return reverse('index')
    template_name = 'result_create.html'
    success_url = 'dashboard'


class DeleteSubjectView(View):
    def get(self, request, pk):
        try:
            get_obj = Subject.objects.get(pk=pk)
            if get_obj.is_active:
                get_obj.is_active = False
            else:
                get_obj.is_active = True

            get_obj.save()
            messages.success(
                request, f"Subject has been deactivated!")
            return HttpResponseRedirect((request.META.get('HTTP_REFERER')))
        except Subject.DoesNotExist:
            messages.error(
                request, f"Deactivating subject failed!")
            return HttpResponseRedirect((request.META.get('HTTP_REFERER')))


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
