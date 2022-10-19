

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.forms import formset_factory

from result.models import Result

from .models import Klass
from .forms import ClassForm

from .models import Klass, Subject
from .forms import ClassForm, ClassLoginForm, SubjectForm
# SubjectForm

from account.models import User
# from result.models import

# Create your views here.


class ClassCreateView(LoginRequiredMixin, CreateView):
    model = Klass
    form_class = ClassForm
    template_name = 'klass/add_class.html'

    def post(self, request, *args, **kwargs):
        print(request.POST)
        class_form = self.form_class(request.POST)

        if class_form.is_valid():
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
        senior_subjects = Subject.objects.filter(level="SENIOR")
        junior_subjects = Subject.objects.filter(level="JUNIOR")
        users = User.objects.filter(is_superuser=False)
        sessions = ["2022/2023", "2023/2024", "2024/2025"]
        return render(request, self.template_name, {
            "login_form": self.form_class(),
            "senior_subject": senior_subjects,
            "junior_subject": junior_subjects,
            "users": users,
            "sessions": sessions
        })


class CreateSubjectView(CreateView):
    login_url = 'login'
    template_name = ""
    form_class = SubjectForm

    def post(self, request, *args, **kwargs):

        SubjectFormset = formset_factory(self.form_class, extra=5)
        subject_formset = SubjectFormset(request.POST)

        if subject_formset.is_valid():
            data = [subject_formset.cleaned_data.items()]
            subjects = Subject.objects.bulk_create(data)

            return HttpResponseRedirect(reverse('class-detail', args=[]))
        else:
            return render(request, "klass/create_subject.html", {
                "subject_formset": subject_formset,
                "errors": subject_formset.errors,
            })

    def get(self, request, *args, **kwargs):
        SubjectFormset = formset_factory(self.form_class, extra=5)
        subject_formset = SubjectFormset()

        return render(request, "klass/create_subject.html", {
            "subject_formset": subject_formset,
        })


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
    # if request.user.is_superuser:
    context["class"] = Klass.objects.select_related('teacher').get(pk=pk)
    # context["results"] = Result.object.all()

    return render(request, 'klass/klass_detail.html', context)


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


def dashboard(request):

    teachers = User.objects.all()
    return render(request, 'klass/landing_page.html', {
        "teachers": teachers})


def admin_teacher_list(request):
    context = {
        "classes": Klass.objects.select_related('teacher').all(),
        "classes": Klass.objects.all().count(),
        "users": User.objects.filter(is_superuser=False).count(),
        # "results": Result.objects.all(),
        "result_count": Result.objects.all().count(),
    }

    return render(request, "klass/admin_teacher_list.html", context)
