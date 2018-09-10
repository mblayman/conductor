from typing import Any

from django import forms
from django.conf import settings

from conductor.planner import tasks
from conductor.planner.models import School, Semester, Student, TargetSchool


class AddSchoolForm(forms.Form):
    school = forms.IntegerField()

    def __init__(self, student: Student, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.student = student

    def clean_school(self) -> None:
        """Check that the student does not already have the selected school."""
        school_id = self.cleaned_data.get("school")
        school = School.objects.get(id=school_id)
        if TargetSchool.objects.filter(student=self.student, school=school).exists():
            raise forms.ValidationError(
                f"{school.name} is already on the student’s list."
            )
        return school

    def save(self) -> None:
        """Create a target school for the student."""
        school = self.cleaned_data["school"]
        TargetSchool.objects.create(student=self.student, school=school)
        tasks.audit_school.delay(school.id, self.student.matriculation_semester_id)


class AddStudentForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    matriculation_semester = forms.ModelChoiceField(
        label="Applying for",
        queryset=Semester.objects.filter(active=True),
        empty_label=None,
    )

    def save(self, user: settings.AUTH_USER_MODEL) -> Student:
        """Create a new student."""
        student = Student.objects.create(
            first_name=self.cleaned_data["first_name"],
            last_name=self.cleaned_data["last_name"],
            matriculation_semester=self.cleaned_data["matriculation_semester"],
            user=user,
        )
        return student
