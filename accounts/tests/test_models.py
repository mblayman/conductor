from conductor.tests import TestCase


class TestUser(TestCase):

    def test_factory(self):
        user = self.UserFactory.build()

        self.assertNotEqual('', user.username)
        self.assertNotEqual('', user.email)
