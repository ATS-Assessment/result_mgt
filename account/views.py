import random
import string
from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

from .forms import RegisterForm
from django import forms

from klass.models import Klass
from result.models import Result, Token

User = get_user_model()


class Home(generic.TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, 'admin_page.html')


class My_Class(generic.View):
    template_name = 'teacher_class.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        teacher = User.objects.filter(role='teacher')

        class_teacher = Klass.objects.filter(
            teacher=user,
        )
        context = {
            'class_teacher': class_teacher,
        }

        class_teacher = Klass.objects.filter(klass__teacher=teacher)


# class CreateTeacherView(generic.View):
#     template_name = 'user.html'

#     def post(self, request, *args, **kwargs):
#         form = TeacherForm(request.POST)
#         context = {
#             'form': form,
#         }
#         if form.is_valid():
#             form.save()
#             messages.success(
#                 request, "A Teacher has been created successfully"
#             )
#             return HttpResponseRedirect(reverse(
#                 request.META.get('HTTP_REFERER'
#                                  )))
#         else:
#             messages.error(request, "Invalid Input")
#         return render(request, self.template_name, context)
class RegisterView(generic.View):
    def get(self, request):
        return render(request, "register.html")

    def post(self, request):
        print(request.POST)
        register_details = RegisterForm(request.POST)
        print(register_details.is_valid())
        # validating form fields
        if register_details.is_valid():
            try:
                # get cleaned data from register form
                email = register_details.cleaned_data['email']
                password = register_details.cleaned_data['password']
                full_name = register_details.cleaned_data['full_name']
                User.objects.create_user(
                    email=email, password=password, full_name=full_name, username='')
                return redirect('login')

            except Exception as e:
                print(e)
                messages.error(
                    self.request, 'Internal server error, please try again later')
                return render(request, "register.html")

        else:

            error = (register_details.errors.as_text()).split('*')
            messages.error(self.request, error[len(error)-1])
            return render(request, "register.html", )


class TeacherSuspendedView(generic.View):
    pass


class UserLogin(generic.View):
    def get(self, request):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(email=email, password=password)

            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return render(request, 'admin_base_template.html')
                else:
                    klass = Klass.objects.filter(
                        teacher=request.user
                    )
                    if klass.exists():
                        class_info = klass.first()


                        return HttpResponseRedirect(reverse("teacher-class-detail", args=[class_info.pk]))
                    else:
                        messages.info(
                            request, 'Hi, you are yet to be assigned a class, if this seems to be an issue, please contact admin')
                        return HttpResponseRedirect(reverse('login'))
            else:
                messages.error(request, "Invalid credentials, try again ")
                return HttpResponseRedirect((request.META.get('HTTP_REFERER')))

        else:
            return render(request, 'login.html')


class UserLogout(generic.View):
    def post(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('home'))


def landing_page(request):
    return render(request, 'klass/landing_page.html',)


class CreateTokenView(generic.View):

    def token_generator(self):
        letters = string.ascii_letters
        digits = string.digits
        random_numbers = random.sample(letters + digits, 10)
        ran_num = ''.join(random_numbers)
        return ran_num

    def get(self, request, *args, **kwargs):
        tokes = Token.objects.all()
        return render(
            request, 'template_name.html', {"tokens": tokes}
        )

    def post(self, request):
        numbers = request.POST.get('number')
        for number in range(numbers + 1):
            Token.objects.create(token=self.token_generator())

        return HttpResponseRedirect(
            (request.META.get('HTTP_REFERER'))
        )


class CheckResultView(generic.View):

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, 'result.html', context)

    def post(self, request, *args, **kwargs):
        admission_num = request.POST.get('admission_number')
        student_token = request.POST.get('token')
        academic_session = request.POST.get('session')

        # token_check = Token.objects.filter(token=student_token).exist()
        result_token = Result.objects.filter(
            admission_number=admission_num,
            session=academic_session,
            result__token=student_token
        ).exist()
        if result_token:
            if result_token != 5:
                result_token.count += 1
            messages.error(request, "A token can not be used more than 5 times")
            return HttpResponseRedirect((request.META.get('HTTP_REFERER')))
        else:
            messages.error(request, "The token number you input is invalid")
            return HttpResponseRedirect((request.META.get('HTTP_REFERER')))








