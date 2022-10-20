from django import forms

from .models import Result


class CreateResultForm(forms.ModelForm):

    class Meta:
        model = Result
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CreateResultForm, self).__init__(*args, **kwargs)

        self.fields["classes"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus: ring-indigo-500 focus: border-indigo-500 sm: text-sm border-gray-700 rounded-md"
        self.fields["current_teacher"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus: ring-indigo-500 focus: border-indigo-500 sm: text-sm border-gray-700 rounded-md"
        self.fields["term"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus: ring-indigo-500 focus: border-indigo-500 sm: text-sm border-gray-700 rounded-md"
        self.fields["session"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus: ring-indigo-500 focus: border-indigo-500 sm: text-sm border-gray-700 rounded-md"
        self.fields["student_name"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm border-gray-700 rounded-md"
        self.fields["guardian_email"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm border-gray-700 rounded-md"
        self.fields["number_of_subjects_taken"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm border-gray-300 rounded-md"
        self.fields["minimum_subjects"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm border-gray-700 rounded-md"
        self.fields["marks_obtained"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm border-gray-700 rounded-md"
        self.fields["number_of_failures"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm border-gray-700 rounded-md"
        self.fields["comment"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm border-gray-700 rounded-md"
        self.fields["term_average"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm border-gray-700 rounded-md"
        self.fields["number_of_passes"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm border-gray-700 rounded-md"
        self.fields["admission_number"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm border-gray-700 rounded-md"
        self.fields["position"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm border-gray-700 rounded-md"
        self.fields["scores"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm border-gray-700 rounded-md"
