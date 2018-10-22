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
    SchoolApplicationFactory,
    SemesterFactory,
    StudentFactory,
    TargetSchoolFactory,
)
from conductor.support.tests.factories import SupportTicketFactory
from conductor.tests.request_factory import RequestFactory
from conductor.trackers.tests.factories import CommonAppTrackerFactory


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
    SchoolApplicationFactory = SchoolApplicationFactory
    SemesterFactory = SemesterFactory
    StudentFactory = StudentFactory
    TargetSchoolFactory = TargetSchoolFactory

    # support
    SupportTicketFactory = SupportTicketFactory

    # trackers
    CommonAppTrackerFactory = CommonAppTrackerFactory
