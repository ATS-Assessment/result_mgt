
from django import forms
from .models import Klass, Subject


class ClassForm(forms.ModelForm):

    class Meta:
        model = Klass
        fields = ('name', 'session', "password")

    def __init__(self, *args, **kwargs):
        super(ClassForm, self).__init__(*args, **kwargs)

        self.fields["name"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"
        # self.fields["teacher"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"
        self.fields["session"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"


class ClassLoginForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        "placeholder": "Enter your Password",
    }))
    username = forms.CharField(max_length=100)

    def __init__(self, *args, **kwargs):
        super(ClassLoginForm, self).__init__(*args, **kwargs)

        self.fields["password"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"
        self.fields["username"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"


class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ("name", "level")

    def __init__(self, *args, **kwargs):
        super(ClassLoginForm, self).__init__(*args, **kwargs)

        self.fields["name"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"
