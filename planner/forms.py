from django import forms

from planner.models import Semester, Student


class AddStudentForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    matriculation_semester = forms.ModelChoiceField(
        label='Applying for',
        queryset=Semester.objects.filter(active=True),
        empty_label=None)

    def save(self, user):
        """Create a new student."""
        Student.objects.create(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            matriculation_semester=self.cleaned_data['matriculation_semester'],
            user=user)
