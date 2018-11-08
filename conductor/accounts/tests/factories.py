from django.conf import settings

import factory

from conductor.accounts import models


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = settings.AUTH_USER_MODEL

    username = factory.Faker("user_name")
    email = factory.Faker("email")


class ProfileFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Profile

    user = factory.SubFactory(UserFactory)


class GoogleDriveAuthFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.GoogleDriveAuth

    user = factory.SubFactory(UserFactory)
    refresh_token = factory.Sequence(lambda n: "refresh token {}".format(n))


class ProductPlanFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.ProductPlan

    stripe_plan_id = factory.Sequence(lambda n: "plan_{}".format(n))
