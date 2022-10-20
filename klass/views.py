

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate, login

from .models import Klass
from .forms import ClassForm

from .models import Klass, Subject
from .forms import ClassForm, ClassLoginForm
from result.models import Result
# SubjectForm

from account.models import User
# from result.models import

# Create your views here.


# def create_class()


class ClassCreateView(LoginRequiredMixin, CreateView):
    model = Klass
    form_class = ClassForm
    template_name = 'klass/add_class.html'

    def search_character(self, characters, request_body):
        data = list(request_body.keys())
        final_data = []
        for char in data:
            if char.startswith(characters) or char.endswith(characters):
                final_data.append(char)
        return final_data

    def find_subjects(self, args, request_body):
        subjects = self.search_character(args, request_body)
        found_subject = []
        for data in subjects:
            found_subject.append(request_body[data])
        return found_subject

    def post(self, request, *args, **kwargs):
        class_name = request.POST.get('class_name', '')
        class_size = request.POST.get('class_size', '')
        educator = request.POST.get('teacher', '')
        session = request.POST.get('session', '')
        dict_object = request.POST.dict()
        subjects = self.find_subjects('subject', dict_object)
        request_body = {
            "name": class_name,
            "no_of_students": class_size,
            "teacher": User.objects.get(full_name=educator),
            "session": session,
            "subjects": subjects
        }

        check_class = Klass.objects.filter(name=class_name)
        if check_class:
            messages.error(
                request, f"A class with name {class_name} already exist")
            return HttpResponseRedirect((request.META.get('HTTP_REFERER')))
        check_teacher = Klass.objects.filter(teacher__full_name=educator)
        if check_teacher:
            messages.error(
                request, f"{educator} has been assigned a class")
            return HttpResponseRedirect((request.META.get('HTTP_REFERER')))
        save_class = Klass(**request_body)
        save_class.save()
        if save_class:
            messages.success(
                self.request, f"{class_name} was successfully created!")
            return HttpResponseRedirect(reverse('admin-class-list'))
        else:
            messages.error(
                request, 'Error creating class, check and try creating class again')
            return HttpResponseRedirect((request.META.get('HTTP_REFERER')))

    def get(self, request):
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


# class CreateSubjectView(CreateView):
#     login_url = 'login'
#     template_name = ""
#     form_class = SubjectForm

#     def post(self, request, *args, **kwargs):
#         subject_data = self.form_class(request.POST)

#         return


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

    def get(self, request, pk):

        return render(request, self.template_name, {
            "login_form": self.form_class(),
            "class": Klass.objects.get(pk=self.kwargs["pk"])
        })


class EditClassAdminView(View):
    template_name = "klass/edit_class_admin.html"

    def get(self, request, pk):
        return render(request, self.template_name, {
            # "login_form": self.form_class(),
            "class": Klass.objects.filter(pk=pk).first()
        })


def class_detail(request, pk):

    context = {}
    # if request.user.is_superuser:
    context["class"] = Klass.objects.select_related('teacher').get(pk=pk)
    # context["results"] = Result.object.all()
    print(context)

    return render(request, 'klass/admin_class_detail.html', context)


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


class AdminDashBoard(View):
    def get(self, request):
        context = {
            "teachers": Klass.objects.select_related('teacher').all(),
            "classes": Klass.objects.all().count(),
            "users": User.objects.filter(is_superuser=False).count(),
            # "results": Result.objects.all(),
            "result_count": Result.objects.all().count(),
        }

        return render(request, "klass/admin_dashboard.html", context)


class AdminClassListView(View):
    def get(self, request):
        context = {
            "classes": Klass.objects.select_related('teacher').all(),
        }

        return render(request, "klass/class_list.html", context)
