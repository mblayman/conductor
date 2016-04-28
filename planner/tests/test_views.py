from conductor.tests import TestCase
from planner import views


class TestSchoolViewSet(TestCase):

    def test_no_create(self):
        """Sanity check that no create method is available."""
        viewset = views.SchoolViewSet()
        self.assertRaises(AttributeError, lambda: viewset.create)
