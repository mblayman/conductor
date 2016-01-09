from django import test

from planner.tests.factories import SchoolFactory


class TestCase(test.TestCase):
    SchoolFactory = SchoolFactory
