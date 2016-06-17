from django import test

from accounts.tests.factories import UserFactory
from planner.tests.factories import MilestoneFactory, SchoolFactory
from support.tests.factories import SupportTicketFactory


class TestCase(test.TestCase):
    # accounts
    UserFactory = UserFactory
    # planner
    MilestoneFactory = MilestoneFactory
    SchoolFactory = SchoolFactory
    # support
    SupportTicketFactory = SupportTicketFactory
