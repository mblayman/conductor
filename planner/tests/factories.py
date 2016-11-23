import datetime

import factory
from faker import Factory

from accounts.tests.factories import UserFactory

fake = Factory.create()


class MilestoneFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'planner.Milestone'

    date = factory.Faker('date_time')


class SchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'planner.School'

    name = factory.LazyAttribute(
        lambda o: '{0} College'.format(fake.last_name_female()))
    slug = factory.Faker('slug')
    url = factory.Faker('url')
    milestones_url = factory.Faker('url')


class SemesterFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'planner.Semester'

    date = factory.LazyFunction(datetime.date.today)


class StudentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'planner.Student'

    user = factory.SubFactory(UserFactory)
    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    matriculation_semester = factory.SubFactory(SemesterFactory)
