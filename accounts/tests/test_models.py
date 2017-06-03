import datetime

from django.db.utils import IntegrityError

from conductor.tests import TestCase


class TestUser(TestCase):

    def test_factory(self):
        user = self.UserFactory.build()

        self.assertNotEqual('', user.username)
        self.assertNotEqual('', user.email)

    def test_unique_email(self):
        self.UserFactory.create(email='matt@test.com')
        with self.assertRaises(IntegrityError):
            self.UserFactory.create(email='matt@test.com')


class TestInviteEmail(TestCase):

    def test_factory(self):
        invite_email = self.InviteEmailFactory.build()

        self.assertNotEqual('', invite_email.email)

    def test_created_date(self):
        invite_email = self.InviteEmailFactory.create()

        self.assertEqual(
            datetime.date.today(), invite_email.created_date.date())
