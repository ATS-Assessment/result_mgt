from django.shortcuts import render, redirect
from django.views import generic
from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from .forms import TeacherForm, UserLoginForm
from django import forms


from klass.models import Klass

User = get_user_model()


class Home(generic.TemplateView):

    def get(self, request, *args, **kwargs):
        return render(request, 'account/index.html')


class My_Class(generic.View):
    template_name = 'teacher_class.html'

    def get(self, request, *args, **kwargs):
        user = request.user
        teacher = User.objects.filter(role='teacher')
        class_teacher = Klass.objects.filter(
            teacher=user,
        )
        context={
            'class_teacher': class_teacher,
        }
        return render(request, self.template_name, context)


class CreateTeacherView(generic.View):
    template_name = 'user.html'

    def post(self, request, *args, **kwargs):
        form = TeacherForm(request.POST)
        context ={
            'form': form,
        }
        if form.is_valid():
            form.save()
            messages.success(
                request, "A Teacher has been created successfully"
            )
            return HttpResponseRedirect(reverse(
                request.META.get('HTTP_REFERER'
            )))
        else:
            messages.error(request, "Invalid Input")
        return render(request, self.template_name, context)


class TeacherSuspendedView(generic.View):
    pass


class UserLogin(generic.View):

    def post(self, request, *args, **kwargs):
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            if user.is_active:
                login(request, user)
                if user.is_superuser:
                    return HttpResponseRedirect(reverse('home'))
                else:
                    klass = Klass.objects.filter(
                        teacher=request.user
                    ).exist()
                    if klass:
                        return HttpResponseRedirect(
                            reverse('class')
                        )
                    return HttpResponseRedirect(
                        reverse('create-class')
                    )
            else:
                messages.error(request, 'You have not logged in')
                return HttpResponseRedirect(reverse('login'))
        return render(request, 'login.html')


class UserLogout(generic.View):
    def post(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('home'))


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('blog-home')
    else:
        form = UserCreationForm()
    return render(request, 'account/register.html', {'form': form})


class All_teachers(generic.View):
    template_name = 'page.html'

    def get(self, request, *args, **kwargs):
        teachers = User.objects.all().exclude(role='admin')
        context = {
            'teachers': teachers
        }
        return render(request, self.template_name, context)
