

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login

<<<<<<< HEAD
from .models import Klass
from .forms import ClassForm
=======

from .models import Klass
from .forms import ClassForm, ClassLoginForm
from account.models import User
>>>>>>> 19cc6f99a844e8d4d3f2cb94d4b489002d67fa75
# from result.models import

# Create your views here.


# def create_class()


class ClassCreateView(LoginRequiredMixin, CreateView):
    model = Klass
    form_class = ClassForm
    template_name = 'class/create.html'

    def post(self, request, *args, **kwargs):
        class_form = self.form_class(request.POST)
        context = {
            'class_form': class_form,
        }
        if class_form.is_valid():
<<<<<<< HEAD
            instance = class_form.save(commit=False)
            password = class_form.cleaned_data.get("password")
    else:

        return render(request, 'klass/add_class.html')
=======
            instance = class_form.save()
            messages.success(
                self.request, f"The Class {instance.name} was successfully created!")
            return HttpResponseRedirect(reverse('class-detail'), args=[instance.pk])
        else:
            messages.error(
                self.request, '')
            return render(request, self.template_name, {"class_form": self.form_class(),
                                                        "errors": class_form.errors})

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "login_form": self.form_class(),
        })
>>>>>>> 19cc6f99a844e8d4d3f2cb94d4b489002d67fa75


class EditClass(LoginRequiredMixin, UpdateView):
    model = Klass
    form_class = ClassForm
    template_name = "klass/edit_klass.html"
    login_url = 'login'

    def post(self, request, *args, **kwargs):
        class_form = self.form_class(request.POST)
        if class_form.is_valid():
            instance = class_form.save()
            messages.success(
                self.request, f"The Class {instance.name} was successfully updated!")
            return HttpResponseRedirect(reverse('class-detail'), args=[instance.pk])
        else:
            messages.error(request, "Invalid Input")
            return render(request, self.template_name, {
                'class_form': self.form_class(),
                "errors": class_form.errors
            })

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "login_form": self.form_class(),
            "class": Klass.objects.get(pk=self.kwargs["pk"])
        })


def class_detail(request, pk):

    context = {}
<<<<<<< HEAD
    if request.user.is_superuser:
        context["classes"] = Klass.objects.select_related('teacher')
        # context["results"] = Result.object.all()
=======
    # if request.user.is_superuser:
    context["class"] = Klass.objects.select_related('teacher').get(pk=pk)
    # context["results"] = Result.object.all()
>>>>>>> 19cc6f99a844e8d4d3f2cb94d4b489002d67fa75

    return render(request, 'klass/klass_detail.html', context)


<<<<<<< HEAD
def class_list(request):
    context = {
        "classes": Klass.objects.all()
    }
    return render(request, 'class-list.html', context)
=======
class ClassLogin(View):
    template_name = "klass/login.html"
    form_class = ClassLoginForm

    def post(self, request, *args, **kwargs):

        login_form = self.form_class(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(
                request, username=username, password=password)
            if user:
                try:
                    klass = Klass.objects.get(teacher=user)
                except Klass.DoesNotExist as e:
                    print(e)

                login(request, user)
                return redirect(reverse("class-detail"), args=[klass.pk])
        else:
            messages.error(request, "Invalid Input")
            return render(request, self.template_name, {
                'class_form': self.form_class(),
                "errors": login_form.errors
            })

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {
            "login_form": self.form_class(),
        })
>>>>>>> 19cc6f99a844e8d4d3f2cb94d4b489002d67fa75
