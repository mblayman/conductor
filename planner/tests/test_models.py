from lcp.tests import TestCase
from planner.models import School


class TestSchool(TestCase):

    def test_has_name(self):
        school = School.objects.create(name='University of Virginia')
        self.assertEqual('University of Virginia', school.name)
