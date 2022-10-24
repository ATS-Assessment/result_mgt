

from django.conf import settings
from django.template.loader import render_to_string
import io
from html import escape
from django.http import HttpResponse
from xhtml2pdf import pisa
from email.message import EmailMessage
from django.core.mail import EmailMultiAlternatives, EmailMessage
from django.shortcuts import render, redirect, HttpResponseRedirect
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DetailView, View, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.forms import formset_factory
from klass.decorators import is_admin, is_teacher

from klass.mixins import AdminOnlyRequiredMixin, EducatorOnlyRequiredMixin

from .models import Klass
from .forms import ClassForm, SubjectForm

from .models import Klass, Subject
from .forms import ClassForm, ClassLoginForm
from result.models import Result, Score
from result.forms import CreateResultForm, ScoreForm
# SubjectForm

from account.models import User
# from result.models import

# Create your views here.


class ClassCreateView(LoginRequiredMixin, AdminOnlyRequiredMixin, CreateView):
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


class CreateSubjectView(LoginRequiredMixin, AdminOnlyRequiredMixin, CreateView):
    login_url = 'login'
    template_name = "klass/create_subject.html"
    form_class = SubjectForm

    def post(self, request, *args, **kwargs):

        SubjectFormset = formset_factory(self.form_class, extra=10)
        subject_formset = SubjectFormset(request.POST)

        if subject_formset.is_valid():
            data = [Subject(**field_dict)
                    for field_dict in subject_formset.cleaned_data]
            print(data)
            subjects = Subject.objects.bulk_create(data)

            return HttpResponseRedirect(reverse("admin-dashboard"))
        else:
            return render(request, self.template_name, {
                "subject_formset": subject_formset,
                "errors": subject_formset.errors,
            })

    def get(self, request, *args, **kwargs):
        SubjectFormset = formset_factory(self.form_class, extra=10)
        subject_formset = SubjectFormset()

        return render(request, "klass/create_subject.html", {
            "subject_formset": subject_formset,
        })


class ResultListView(LoginRequiredMixin, EducatorOnlyRequiredMixin, ListView):
    model = Result
    template_name = 'klass/result_list.html'
    context_object_name = 'results'

    def get_queryset(self):
        return Result.objects.filter(current_teacher__pk=self.request.user.pk, is_inactive=False)


class SubjectListView(LoginRequiredMixin, AdminOnlyRequiredMixin, ListView):
    model = Result
    template_name = 'klass/subject_list.html'
    context_object_name = 'subjects'

    def get_queryset(self):
        return Subject.objects.all()


class EditClass(LoginRequiredMixin, EducatorOnlyRequiredMixin, UpdateView):
    model = Klass
    form_class = ClassForm
    template_name = "klass/edit_klass.html"
    login_url = 'login'

    def post(self, request, pk=None, *args, **kwargs):
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
        # pk = self.kwargs.get("pk")
        return render(request, self.template_name, {
            "edit_form": self.form_class(),
            "class": Klass.objects.get(pk=pk)
        })


class EditResult(LoginRequiredMixin, EducatorOnlyRequiredMixin, UpdateView):
    model = Result
    form_class = CreateResultForm
    template_name = "klass/edit_result.html"
    login_url = 'login'

    def post(self, request, pk=None, *args, **kwargs):
        result_form = self.form_class(request.POST)
        if result_form.is_valid():
            instance = result_form.save()
            messages.success(
                self.request, f"The Result with {instance.admission_number} was successfully updated!")
            return HttpResponseRedirect(reverse('result-detail'), args=[instance.pk])
        else:
            messages.error(request, "Invalid Input")
            return render(request, self.template_name, {
                'form': self.form_class(),
                "errors": result_form.errors
            })

    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk")
        return render(request, self.template_name, {
            "form": self.form_class(request.POST),
            "result": Result.objects.get(pk=pk)
        })


def toggle_delete_result(request, pk):
    result = Result.objects.get(pk=pk)
    result.is_inactive = not result.is_inactive
    return redirect("result-list")


class EditClassAdminView(LoginRequiredMixin, AdminOnlyRequiredMixin, View):
    template_name = "klass/edit_class_admin.html"

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

    def post(self, request, pk):
        class_name = request.POST.get('class_name', '')
        class_size = request.POST.get('class_size', '')
        educator = request.POST.get('teacher', '')
        session = request.POST.get('session', '')
        dict_object = request.POST.dict()
        subjects = self.find_subjects('subject', dict_object)
        class_instance = Klass.objects.get(pk=pk)
        class_instance.name = class_name
        class_instance.no_of_students = class_size
        class_instance.teacher = User.objects.get(full_name=educator)
        class_instance.session = session
        class_instance.subjects = subjects

        klass = Klass.objects.get(pk=pk)

        if klass.teacher.full_name != educator:
            teacher_dict = {
                'name': klass.teacher.full_name,
                'session': klass.session
            }
            pre_teacher = [class_instance.previous_teachers].append(
                teacher_dict)

            class_instance.previous_teachers = pre_teacher

        check_teacher = Klass.objects.filter(teacher__full_name=educator)
        if check_teacher:
            messages.error(
                request, f"{educator} has been assigned a class")
            return HttpResponseRedirect((request.META.get('HTTP_REFERER')))

        class_instance.save()

        return HttpResponseRedirect((request.META.get('HTTP_REFERER')))

    def get(self, request, pk):

        return render(request, self.template_name, {
            # "login_form": self.form_class(),
            "class": Klass.objects.filter(pk=pk).first(),
            "users": User.objects.filter(is_superuser=False),
            "sessions": ["2022/2023", "2023/2024", "2024/2025"],
            "senior_subjects": Subject.objects.filter(level="SENIOR"),
            "junior_subjects": Subject.objects.filter(level="JUNIOR")
        })


@login_required(login_url='login')
@is_admin
def class_detail(request, pk):

    context = {}
    # if request.user.is_superuser:
    context["class"] = Klass.objects.get(pk=pk)
    # context["results"] = Result.object.all()
    print(context)

    return render(request, 'klass/admin_class_detail.html', context)


@login_required(login_url="login")
@is_teacher
def teacher_class_detail(request):

    context = {}

    context["class"] = Klass.objects.get(teacher=request.user)
    print(context)

    return render(request, 'klass/klass_detail.html', context)


# def test(request):
#     ;

class CreateResultView(LoginRequiredMixin, EducatorOnlyRequiredMixin, CreateView):
    model = Result
    form_class = CreateResultForm
    template_name = 'klass/result_create.html'

    def search_character(self, characters, request_body):
        data = list(request_body.keys())
        final_data = []
        for char in data:
            if char.startswith(characters) or char.endswith(characters):
                final_data.append(char)
        return final_data

    def find_result(self, subject_arr, request_body):
        q = request_body
        for char in subject_arr:
            l = self.search_character(char, request_body)
            obj = {}
            for x in l:
                key = x.split('-')
                obj[key[len(key) - 1]] = q.get(x)
            return obj

    def post(self, request, *args, **kwargs):
        result_form = self.form_class(request.POST)
        teacher = User.objects.get(pk=request.user.id)
        class_detail = Klass.objects.get(teacher__pk=teacher.pk)

        check_result = Result.objects.filter(admission_number=request.POST['admission_number'],
                                             session=class_detail.session, term=request.POST['term'])
        if check_result.exists():
            messages.error(
                request, f"A result with same detail, is already available ")
            return HttpResponseRedirect((request.META.get('HTTP_REFERER')))

        result_instance = {
            "classes": Klass.objects.get(pk=class_detail.id),
            "student_name": request.POST['student_name'],
            "admission_number": request.POST['admission_number'],
            "term": request.POST['term'],
            "session": class_detail.session,
            "position": request.POST['position'],
            "current_teacher": teacher,
            "minimum_subjects": request.POST['minimum_subjects'],
            "minimum_marks": request.POST['minimum_marks'],
            "marks_obtained": request.POST['marks_obtained'],
            "term_average": request.POST['term_average'],
            "comment": request.POST['comment'],
            "guardian_email": request.POST['guardian_email'],
            "number_of_subjects_taken": request.POST.get('number_of_subjects_taken', 1),
            "number_of_passes": request.POST.get("number_of_passes", 1),
            "number_of_failures": request.POST.get('number_of_failures', 1)
        }

        new_result = Result(**result_instance)
        new_result.save()
        print(result_instance)

        class_subjects = Klass.objects.filter(
            teacher__pk=request.user.id).first()

        subject_arr = class_subjects.subjects
        # result_subject = self.find_result(subject_arr, request.POST.dict())

        for char in subject_arr:
            l = self.search_character(char, request.POST.dict())
            obj = {}
            for x in l:
                key = x.split('-')
                obj[key[len(key) - 1]] = request.POST.dict().get(x)
                obj['subject_name'] = x.replace((key[len(key) - 1]), '')
            result_score = Score(
                result=Result.objects.get(pk=new_result.pk), **obj)
            result_score.save()

        return HttpResponseRedirect((request.META.get('HTTP_REFERER')))

    def get(self, request, *args, **kwargs):
        result_form = self.form_class()
        score_form = ScoreForm()
        print(request.user)
        class_subjects = Klass.objects.filter(
            teacher__pk=request.user.id).first()
        print(class_subjects.subjects)

        return render(request, self.template_name, {
            "form": result_form,
            "class_info": class_subjects,
            "score_form": score_form,
            "class_subjects": class_subjects.subjects
        })


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


class ClassLogout(LoginRequiredMixin, View):
    def post(self, request):
        logout(request)
        return HttpResponseRedirect('home')


class AdminDashBoard(LoginRequiredMixin, AdminOnlyRequiredMixin, View):
    def get(self, request):
        context = {
            "teachers": Klass.objects.select_related('teacher').all(),
            "classes": Klass.objects.all().count(),
            "users": User.objects.filter(is_superuser=False).count(),
            # "results": Result.objects.all(),
            "result_count": Result.objects.all().count(),
        }

        return render(request, "klass/klass_detail.html", context)


class AdminDashBoardView(View):
    def get(self, request):
        context = {
            "teachers": Klass.objects.all(),
            "classes": Klass.objects.all().count(),
            "users": User.objects.filter(is_superuser=False).count(),
        }
        return render(request, 'klass/admin_dashboard.html', context)


class EducatorDashBoard(LoginRequiredMixin, EducatorOnlyRequiredMixin, View):
    def get(self, request):
        context = {
            "teachers": Klass.objects.select_related('teacher').all(),
            "class": Klass.objects.get(teacher=request.user),

            # "results": Result.objects.all(),
            "result_count": Result.objects.all().count(),
        }

        return render(request, "klass/admin_dashboard.html", context)


def results(request):
    results = Result.objects.filter(current_teacher__pk=request.user.pk)

    return render(request, "klass/klass_detail.html", context)


@ login_required(login_url="login")
@ is_teacher
def result_detail(request, pk):
    result = Result.objects.get(current_teacher__pk=request.user.pk, pk=pk)
    score = Score.objects.filter(result=result)

    return render(request, 'klass/result_detail.html', {
        "result": result,
        "score": score})


def render_to_pdf(template_src, context_dict):
    html = render_to_string(template_src, context_dict)
    result = io.BytesIO()

    pdf = pisa.pisaDocument(io.BytesIO(html.encode("utf-8")), result)
    print(pdf, "Ok")
    if not pdf.err:
        return result.getvalue()
    return HttpResponse('We had some errors<pre>%s</pre>' % escape(html))


def generate_pdf(request, pk):
    result = Result.objects.get(pk=pk)
    context = {
        "results": Score.objects.filter(result__pk=pk),
        "info": result
    }
    pdf = render_to_pdf(
        'klass/result_details.html',
        {
            'pagesize': 'A4',
            "results": Score.objects.filter(result__pk=pk),
            "info": result
        }

    )
    print("Here", pdf)
    mail_address = [result.guardian_email]
    from_email = settings.DEFAULT_FROM_EMAIL
    subject = "Termly Result Of your Ward"
    message = "Dear Sir/Madam, Please find attached is a copy of your wards result for this term(in PDF format). We appreciate your trust and confidence in our capacities and capabilities to train and nurture your ward. We can't wait to welcome them back next term! Have an amazing holiday and Happy Halloween in Advance!."

    email_message = EmailMessage(
        subject,
        message,
        to=mail_address,
        from_email=from_email,
    )
    filename = 'Result.pdf'
    mimetype_pdf = 'application/pdf'
    email_message.attach(filename, pdf, mimetype_pdf)
    email_message.send(fail_silently=False)  #

    messages.success(
        request, f"Result has been successfully sent to the parent/guardian's email!")
    return HttpResponseRedirect((request.META.get('HTTP_REFERER')))
    # return HttpResponse(pdf, content_type='application/pdf')


class AdminClassListView(AdminOnlyRequiredMixin, View):
    def get(self, request):
        context = {
            "classes": Klass.objects.select_related('teacher').all(),
        }

        return render(request, "klass/class_list.html", context)


def page_404(request, exception=None):
    return render(request, "klass/404.html")


def page_403(request, exception=None):
    return render(request, "klass/403.html")


def page_500(request, exception=None):
    return render(request, "klass/500.html")
