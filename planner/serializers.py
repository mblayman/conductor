from rest_framework.validators import UniqueTogetherValidator
from rest_framework_json_api import serializers

from planner.models import (
    ApplicationStatus, Milestone, School, Semester, Student, TargetSchool)


class ApplicationStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = ApplicationStatus
        fields = (
            'id',
            'created_date',
            'student'
        )


class MilestoneSerializer(serializers.ModelSerializer):
    class Meta:
        model = Milestone
        fields = ('id', 'date', 'category')


class SchoolSerializer(serializers.ModelSerializer):
    # XXX: Filtering milestones to active=True with a ResourceRelatedField
    # does not seem to work. This will be a problem once some dates need
    # to be eclipsed.

    included_serializers = {
        'milestones': MilestoneSerializer,
    }

    class Meta:
        model = School
        fields = ('id', 'name', 'milestones')

    class JSONAPIMeta:
        included_resources = ['milestones']


class SemesterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Semester
        fields = ('id', 'date')


class StudentSerializer(serializers.ModelSerializer):
    included_serializers = {
        'matriculation_semester': SemesterSerializer,
        'schools': SchoolSerializer,
    }

    class Meta:
        model = Student
        fields = (
            'id',
            'first_name',
            'last_name',
            'matriculation_semester',
            'schools',
        )

    class JSONAPIMeta:
        included_resources = ['matriculation_semester', 'schools']


class TargetSchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetSchool
        fields = ('id', 'school', 'student')
        validators = [
            UniqueTogetherValidator(
                queryset=TargetSchool.objects.all(),
                fields=('school', 'student')
            )
        ]
