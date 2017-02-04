import datetime

from conductor.tests import TestCase


class TestUser(TestCase):

    def test_factory(self):
        user = self.UserFactory.build()

        self.assertNotEqual('', user.username)
        self.assertNotEqual('', user.email)


class TestInviteEmail(TestCase):

    def test_factory(self):
        invite_email = self.InviteEmailFactory.build()

        self.assertNotEqual('', invite_email.email)

    def test_created_date(self):
        invite_email = self.InviteEmailFactory.create()

        self.assertEqual(
            datetime.date.today(), invite_email.created_date.date())
