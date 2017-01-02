from django import test

from accounts.tests.factories import InviteEmailFactory, UserFactory
from conductor.tests.request_factory import RequestFactory
from planner.tests.factories import (
    MilestoneFactory, SchoolFactory, SemesterFactory, StudentFactory,
    TargetSchoolFactory)
from support.tests.factories import SupportTicketFactory


class TestCase(test.TestCase):
    request_factory = RequestFactory()

    # accounts
    InviteEmailFactory = InviteEmailFactory
    UserFactory = UserFactory
    # planner
    MilestoneFactory = MilestoneFactory
    SchoolFactory = SchoolFactory
    SemesterFactory = SemesterFactory
    StudentFactory = StudentFactory
    TargetSchoolFactory = TargetSchoolFactory
    # support
    SupportTicketFactory = SupportTicketFactory
