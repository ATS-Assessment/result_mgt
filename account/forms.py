import string

from django import forms

from .models import User
from django.utils.translation import gettext_lazy as _


class TeacherForm(forms.ModelForm):
    pass

    # class Meta:
    #     model = User
    #     fields = ('__all__',)
    #     labels = {
    #         "password1": 'Password',
    #         "password2": 'Confirm Password'
    #     }
    #
    # def clean(self):
    #     name = self.cleaned_data.get('name')
    #
    #     if len(name) < 5:
    #         self._errors['username'] = self.error_class([
    #             'Minimum 5 characters required'
    #         ])
# class TeacherForm(forms.ModelForm):

#     class Meta:
#         model = User
#         fields = (
#             'name',
#             'password1',
#             'password2',
#         )
#         labels = {
#             "password1": 'Password',
#             "password2": 'Confirm Password'
#         }

#     def clean(self):
#         name = self.cleaned_data.get('name')

#         if len(name) < 5:
#             self._errors['username'] = self.error_class([
#                 'Minimum 5 characters required'
#             ])


class RegisterForm(forms.Form):
    full_name = forms.CharField(max_length=255, required=True)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(
        label='Confirm Password', widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super(RegisterForm, self).clean()
        email: str = cleaned_data.get('email')
        password: str = cleaned_data.get("password")
        password_2: str = cleaned_data.get("confirm_password")

        qs = User.objects.filter(email=email).exists()
        if qs:
            raise forms.ValidationError(
                _(f"a user with {email} already exists"), code=409)

        if len(password) < 8:
            raise forms.ValidationError(
                _(f"Password must be at least 8 characters"))

        if password is not None and password != password_2:
            raise forms.ValidationError(_(f"Both passwords must match"))

        return cleaned_data
