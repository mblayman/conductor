from django import test

from conductor.accounts.tests.factories import (
    GoogleDriveAuthFactory,
    ProfileFactory,
    UserFactory,
)
from conductor.planner.tests.factories import (
    ApplicationScheduleFactory,
    AuditFactory,
    MilestoneFactory,
    SchoolFactory,
    SemesterFactory,
    StudentFactory,
    TargetSchoolFactory,
)
from conductor.support.tests.factories import SupportTicketFactory
from conductor.tests.request_factory import RequestFactory


class TestCase(test.TestCase):
    request_factory = RequestFactory()

    # accounts
    GoogleDriveAuthFactory = GoogleDriveAuthFactory
    ProfileFactory = ProfileFactory
    UserFactory = UserFactory

    # planner
    ApplicationScheduleFactory = ApplicationScheduleFactory
    AuditFactory = AuditFactory
    MilestoneFactory = MilestoneFactory
    SchoolFactory = SchoolFactory
    SemesterFactory = SemesterFactory
    StudentFactory = StudentFactory
    TargetSchoolFactory = TargetSchoolFactory

    # support
    SupportTicketFactory = SupportTicketFactory
