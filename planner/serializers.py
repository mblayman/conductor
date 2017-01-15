from rest_framework.validators import UniqueTogetherValidator
from rest_framework_json_api import serializers

from planner.models import School, Semester, Student, TargetSchool


class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('id', 'name')


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
        # XXX: Side loading is currently broken in DJA.
        # See https://github.com/django-json-api/django-rest-framework-json-api/issues/291
        included_resources = ['matriculation_semester']


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
