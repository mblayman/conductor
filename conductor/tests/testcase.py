from django import test

from planner.tests.factories import MilestoneFactory, SchoolFactory
from support.tests.factories import SupportTicketFactory


class TestCase(test.TestCase):
    # planner
    MilestoneFactory = MilestoneFactory
    SchoolFactory = SchoolFactory
    # support
    SupportTicketFactory = SupportTicketFactory
