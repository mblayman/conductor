from django import test

from planner.tests.factories import MilestoneFactory, SchoolFactory


class TestCase(test.TestCase):
    MilestoneFactory = MilestoneFactory
    SchoolFactory = SchoolFactory
