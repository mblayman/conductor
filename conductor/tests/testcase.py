from django import test

from accounts.tests.factories import ProfileFactory, UserFactory
from conductor.tests.request_factory import RequestFactory
from planner.tests.factories import (
    AuditFactory, MilestoneFactory, ScheduleFactory, SchoolFactory,
    SemesterFactory, StudentFactory, TargetSchoolFactory)
from support.tests.factories import SupportTicketFactory


class TestCase(test.TestCase):
    request_factory = RequestFactory()

    # accounts
    ProfileFactory = ProfileFactory
    UserFactory = UserFactory

    # planner
    AuditFactory = AuditFactory
    MilestoneFactory = MilestoneFactory
    ScheduleFactory = ScheduleFactory
    SchoolFactory = SchoolFactory
    SemesterFactory = SemesterFactory
    StudentFactory = StudentFactory
    TargetSchoolFactory = TargetSchoolFactory

    # support
    SupportTicketFactory = SupportTicketFactory
