import string

from django import forms

from .models import User


class TeacherForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'name',
            'password1',
            'password2',
        )
        labels = {
            "password1": 'Password',
            "password2": 'Confirm Password'
        }

    def clean(self):
        name = self.cleaned_data.get('name')

        if len(name) < 5:
            self._errors['username'] = self.error_class([
                'Minimum 5 characters required'
            ])


class UserLoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = (
            'username',
            'password'
        )


