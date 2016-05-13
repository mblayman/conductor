import factory


class SupportTicketFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = 'support.SupportTicket'

    subject = factory.Faker('sentence')
    message = factory.Faker('text')
