from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

from .forms import TeacherForm, UserLoginForm
from django import forms

from klass.models import Klass

User = get_user_model()


class Home(generic.TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, 'admin_page.html')


class My_Class(generic.View):

    def get(self, request, *args, **kwargs):
        user = request.user
        teacher = User.objects.filter(role='teacher')
        class_teacher = Klass.objects.filter(klass__teacher=teacher)


class CreateTeacherView(generic.View):
    template_name = 'user.html'

    def post(self, request, *args, **kwargs):
        form = TeacherForm(request.POST)
        context ={
            'form': form,
        }
        if form.is_valid():
            form.save()
            messages.success(request, "A Teacher has been created successfully")
            return HttpResponseRedirect(reverse(request.META.get('HTTP_REFERER')))
        else:
            messages.error(request, "Invalid Input")
        return render(request, self.template_name, context)


class UserLogout(generic.View):

    def post(self, request, *args, **kwargs):
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    login(request, user)
                    admin = User.objects.filter(user_role='admin')
                    if admin:
                        return HttpResponseRedirect(reverse('home'))
                    else:
                        return HttpResponseRedirect(reverse('class'))
                else:
                    messages.error(request, 'You have not logged in')
            else:
                return HttpResponse("Username or password is not correct ")
        else:
            return render(request, 'login.html')


class UserLogout(generic.View):
    def post(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('home'))



