

from django.shortcuts import render, redirect
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import Klass
from .forms import ClassForm
# from result.models import

# Create your views here.


# def create_class()


# class ClassCreateView(LoginRequiredMixin, CreateView):
#     model = Class
#     form_class = ClassForm
#     template_name = 'class/create.html'

#     def form_valid(self, form):
#         instance = form.save(commit=False)
#         instance.save()
#         messages.success(
#             self.request, 'The Class was successfully created!')
#         return redirect('class-detail')

def create_class(request):
    if request.method == 'POST':
        class_form = ClassForm(request.POST)
        if class_form.is_valid():
            instance = class_form.save(commit=False)
            password = class_form.cleaned_data.get("password")
    else:

        return render(request, 'klass/add_class.html')


class EditClass(LoginRequiredMixin, UpdateView):
    model = Klass
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
        context["classes"] = Klass.objects.select_related('teacher')
        # context["results"] = Result.object.all()

    return render(request, 'class-detail.html', context)


def class_list(request):
    context = {
        "classes": Klass.objects.all()
    }
    return render(request, 'class-list.html', context)
