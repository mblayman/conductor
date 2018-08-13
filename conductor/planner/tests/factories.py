import datetime
from typing import Any, List

import factory
from faker import Factory

from conductor.accounts.tests.factories import UserFactory
from conductor.planner.models import School

fake = Factory.create()


class ApplicationStatusFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "planner.ApplicationStatus"

    student = factory.SubFactory("conductor.planner.tests.factories.StudentFactory")


class SchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "planner.School"

    name = factory.LazyAttribute(
        lambda o: "{0} College".format(fake.last_name_female())
    )
    slug = factory.Faker("slug")
    url = factory.Faker("url")
    milestones_url = factory.Faker("url")
    image = factory.django.FileField()


class MilestoneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "planner.Milestone"

    date = factory.Faker("date")
    school = factory.SubFactory(SchoolFactory)


class AuditFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "planner.Audit"

    school = factory.SubFactory(SchoolFactory)


class SemesterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "planner.Semester"

    date = factory.LazyFunction(datetime.date.today)


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "planner.Student"

    user = factory.SubFactory(UserFactory)
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    matriculation_semester = factory.SubFactory(SemesterFactory)

    @factory.post_generation
    def schools(self, create: bool, extracted: List[School], **kwargs: Any) -> None:
        if not create:
            return

        if extracted:
            for school in extracted:
                TargetSchoolFactory.create(student=self, school=school)


class TargetSchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "planner.TargetSchool"

    school = factory.SubFactory(SchoolFactory)
    student = factory.SubFactory(StudentFactory)
