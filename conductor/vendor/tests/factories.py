import factory
from faker import Factory

from conductor.vendor.models import PromptSchool

fake = Factory.create()


class PromptSchoolFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PromptSchool

    name = factory.LazyAttribute(
        lambda o: "{0} College".format(fake.last_name_female())
    )
    slug = factory.Faker("slug")
