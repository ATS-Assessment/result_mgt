

from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import Class
from .forms import ClassForm
# from result.models import

# Create your views here.


# def create_class()


class ClassCreateView(LoginRequiredMixin, CreateView):
    model = Class
    form_class = ClassForm
    template_name = 'class/create.html'

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.save()
        messages.success(
            self.request, 'The Class was successfully created!')
        return redirect('class-detail')


class EditClass(LoginRequiredMixin, UpdateView):
    model = Class
    form_class = ClassForm
    template_name = "class/edit.html"

    def form_valid(self, form):
        instance = form.save()
        messages.success(
            self.request, 'The Class was successfully created!')
        return redirect('class-detail')


def class_detail_admin_teacher(request):

    context = {}
    if request.user.is_superuser:
        context["classes"] = Class.objects.select_related('teacher')
        context["results"] = Result.object.all()

    return render(request, 'class-detail.html', context)


def class_list(request):
    context = {
        "classes": Class.objects.all()
    }
    return render(request, 'class-list.html', context)
