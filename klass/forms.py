
from django import forms
from .models import Klass, Subject


class ClassForm(forms.ModelForm):

    class Meta:
        model = Klass
        fields = ('name', 'no_of_students', 'session', 'subjects')

    def __init__(self, *args, **kwargs):
        super(ClassForm, self).__init__(*args, **kwargs)

        self.fields["name"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-gray-500 focus:border-gray-500 sm:text-sm border-gray-300 rounded-md border-b-2"
        self.fields["no_of_students"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus: ring-gray-500 focus: border-gray-500 sm: text-sm border-gray-300 rounded-md border-b-2"
        self.fields["session"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus: ring-gray-500 focus: border-gray-500 sm: text-sm border-gray-300 rounded-md border-b-2"
        self.fields["subjects"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus: ring-gray-500 focus: border-gray-500 sm: text-sm border-gray-300 rounded-md border-b-2"


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
        fields = "__all__"
        model = Subject

    def __init__(self, *args, **kwargs):
        super(SubjectForm, self).__init__(*args, **kwargs)

        self.fields["name"].widget.attrs["class"] = "mt-1 p-2 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 border-b-2 border-black"
        self.fields["level"].widget.attrs["class"] = "mt-1 p-2 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 border-1 border-black border"
