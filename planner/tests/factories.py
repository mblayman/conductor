import factory
from faker import Factory

fake = Factory.create()


class SchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'planner.School'

    name = factory.LazyAttribute(
        lambda o: '{0} College'.format(fake.last_name_female()))
