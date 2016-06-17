from conductor.tests import TestCase


class TestUser(TestCase):

    def test_factory(self):
        user = self.UserFactory.build()

        self.assertNotEqual('', user.username)
        self.assertNotEqual('', user.email)

    def test_has_email(self):
        user = self.UserFactory.build(email='jane.doe@nowhere.com')
        self.assertEqual('jane.doe@nowhere.com', user.email)
