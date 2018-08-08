from django.db.utils import IntegrityError

from conductor.tests import TestCase


class TestUser(TestCase):
    def test_factory(self):
        user = self.UserFactory.build()

        self.assertNotEqual("", user.username)
        self.assertNotEqual("", user.email)

    def test_unique_email(self):
        self.UserFactory.create(email="matt@test.com")
        with self.assertRaises(IntegrityError):
            self.UserFactory.create(email="matt@test.com")

    def test_has_profile(self):
        user = self.UserFactory.create()

        self.assertIsNotNone(user.profile)

    def test_has_google_drive_auth(self):
        user = self.UserFactory.create()
        self.GoogleDriveAuthFactory.create(user=user)

        self.assertTrue(user.has_google_drive_auth)

    def test_has_google_drive_auth_missing(self):
        user = self.UserFactory.create()

        self.assertFalse(user.has_google_drive_auth)


class TestProfile(TestCase):
    def test_factory(self):
        profile = self.ProfileFactory.build()

        self.assertIsNotNone(profile.user)
        self.assertEqual("", profile.postal_code)
        self.assertEqual("", profile.stripe_customer_id)

    def test_has_postal_code(self):
        profile = self.ProfileFactory.build(postal_code="21702")

        self.assertEqual("21702", profile.postal_code)

    def test_has_stripe_customer_id(self):
        profile = self.ProfileFactory.build(stripe_customer_id="cus_1234")

        self.assertEqual("cus_1234", profile.stripe_customer_id)


class TestGoogleDriveAuth(TestCase):
    def test_factory(self):
        auth = self.GoogleDriveAuthFactory.create()

        self.assertIsNotNone(auth.user)
        self.assertIsNotNone(auth.created_date)

    def test_has_user(self):
        user = self.UserFactory.build()
        auth = self.GoogleDriveAuthFactory.build(user=user)

        self.assertEqual(user, auth.user)

    def test_has_token(self):
        token = "fake_authorization_token"
        auth = self.GoogleDriveAuthFactory.build(token=token)

        self.assertEqual(token, auth.token)

    def test_has_refresh_token(self):
        refresh_token = "fake_authorization_refresh_token"
        auth = self.GoogleDriveAuthFactory.build(refresh_token=refresh_token)

        self.assertEqual(refresh_token, auth.refresh_token)

    def test_has_id_token(self):
        id_token = "fake_authorization_id_token"
        auth = self.GoogleDriveAuthFactory.build(id_token=id_token)

        self.assertEqual(id_token, auth.id_token)
