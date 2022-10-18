
from django import forms
from .models import Class


class ClassForm(forms.ModelForm):

    class Meta:
        model = Class
        fields = ('name', 'teacher', 'session',"password")

    def __init__(self, *args, **kwargs):
        super(ClassForm, self).__init__(*args, **kwargs)

        self.fields["name"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"
        self.fields["teacher"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"
        self.fields["session"].widget.attrs["class"] = "mt-1 focus: ring-cyan-500 focus: border-cyan-500 block w-full shadow-sm sm: text-sm border-gray-300 rounded-md"
