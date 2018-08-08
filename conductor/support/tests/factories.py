import factory


class SupportTicketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = "support.SupportTicket"

    email = factory.Faker("email")
    subject = factory.Faker("sentence")
    message = factory.Faker("text")
