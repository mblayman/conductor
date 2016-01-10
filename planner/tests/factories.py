import factory
from faker import Factory

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
    url = factory.Faker('url')
    milestones_url = factory.Faker('url')
