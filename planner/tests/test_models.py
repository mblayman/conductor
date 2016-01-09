from lcp.tests import TestCase


class TestSchool(TestCase):

    def test_has_name(self):
        school = self.SchoolFactory.build(name='University of Virginia')
        self.assertEqual('University of Virginia', school.name)

    def test_has_url(self):
        school = self.SchoolFactory.build(url='http://www.virginia.edu/')
        self.assertEqual('http://www.virginia.edu/', school.url)
