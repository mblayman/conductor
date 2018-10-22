import factory
from faker import Factory

from conductor.trackers.models import CommonAppTracker

fake = Factory.create()


class CommonAppTrackerFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CommonAppTracker

    name = factory.LazyAttribute(
        lambda o: "{0} College".format(fake.last_name_female())
    )
    slug = factory.Faker("slug")
