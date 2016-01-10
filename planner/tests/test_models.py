import datetime

from lcp.tests import TestCase


class TestMilestone(TestCase):

    def test_has_date(self):
        date = datetime.datetime.now()
        milestone = self.MilestoneFactory.build(date=date)
        self.assertEqual(date, milestone.date)


class TestSchool(TestCase):

    def test_has_name(self):
        school = self.SchoolFactory.build(name='University of Virginia')
        self.assertEqual('University of Virginia', school.name)

    def test_has_url(self):
        school = self.SchoolFactory.build(url='http://www.virginia.edu/')
        self.assertEqual('http://www.virginia.edu/', school.url)

    def test_has_milestones_url(self):
        school = self.SchoolFactory.build(
            milestones_url='http://admission.virginia.edu/events')
        self.assertEqual(
            'http://admission.virginia.edu/events', school.milestones_url)
