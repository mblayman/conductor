from django import forms

from planner.models import Semester


class AddStudentForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    matriculation_semester = forms.ModelChoiceField(
        label='Applying for',
        queryset=Semester.objects.filter(active=True),
        empty_label=None)
