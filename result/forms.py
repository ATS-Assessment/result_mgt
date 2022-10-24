from django import forms

from .models import Result, Score


class CreateResultForm(forms.ModelForm):

    class Meta:
        model = Result
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(CreateResultForm, self).__init__(*args, **kwargs)

        self.fields["classes"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus: ring-gray-500 focus: border-gray-500 sm: text-sm border-gray-700  border-b-2 border-gray-900"
        # self.fields["current_teacher"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus: ring-gray-500 focus: border-gray-500 sm: text-sm border-gray-700 border-b-2 "
        self.fields["term"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus: ring-gray-500 focus: border-gray-500 sm: text-sm border-gray-700  border-b-2 "
        self.fields["session"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus: ring-gray-500 focus: border-gray-500 sm: text-sm border-gray-700 border-b-2 "
        # self.fields["position"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus: ring-gray-500 focus: border-gray-500 sm: text-sm border-gray-700 border-b-2 "
        self.fields["student_name"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-gray-500 focus:border-gray-500 sm:text-sm border-gray-700 border-b-2 "
        self.fields["guardian_email"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-gray-500 focus:border-gray-500 sm:text-sm border-gray-700 border-b-2 "
        self.fields["term"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-gray-500 focus:border-gray-500 sm:text-sm border-gray-700 border-b-2 "
        self.fields["number_of_subjects_taken"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-gray-500 focus:border-gray-500 sm:text-sm border-gray-300 border-b-2 "
        self.fields["minimum_subjects"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-gray-500 focus:border-gray-500 sm:text-sm border-gray-700 border-b-2 "
        self.fields["marks_obtained"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-gray-500 focus:border-gray-500 sm:text-sm border-gray-700 border-b-2 "
        self.fields["number_of_failures"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-gray-500 focus:border-gray-500 sm:text-sm border-gray-700 border-b-2 "
        self.fields["comment"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-gray-500 focus:border-gray-500 sm:text-sm border-gray-700 border-b-2 "
        self.fields["term_average"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-gray-500 focus:border-gray-500 sm:text-sm border-gray-700 border-b-2 "
        self.fields["number_of_passes"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-gray-500 focus:border-gray-500 sm:text-sm border-gray-700 border-b-2 "
        self.fields["minimum_marks"].widget.attrs["class"] = "rounded-md block max-w-lg w-full shadow-sm focus:ring-gray-500 focus:border-gray-500 sm:text-sm border-gray-700 border-b-2 "
        self.fields["admission_number"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-gray-500 focus:border-gray-500 sm:text-sm border-gray-700 border-b-2 "
        self.fields["position"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-gray-500 focus:border-gray-500 sm:text-sm border-gray-700 border-b-2 "
        # self.fields["scores"].widget.attrs["class"] = "block max-w-lg w-full shadow-sm focus:ring-gray-500 focus:border-gray-500 sm:text-sm border-gray-700 rounded-md"


class ScoreForm(forms.ModelForm):
    class Meta:
        model = Score
        fields = "__all__"
