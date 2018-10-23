from typing import List

from conductor.trackers.models import CommonAppTracker, RawCommonAppSchool


class CommonAppHandler:
    """Process the common app schools that were fetched from the website."""

    def handle(self, common_app_schools: List[RawCommonAppSchool]) -> None:
        """Handle each school to add to tracking if needed."""
        # Assume that if the count matches, then the database is current.
        if len(common_app_schools) == CommonAppTracker.objects.count():
            return

        for raw_common_app_school in common_app_schools:
            self.process_school(raw_common_app_school)

    def process_school(self, raw_common_app_school: RawCommonAppSchool) -> None:
        """Process the raw school into a tracked school.

        Track the add/mod/delete status compared to the database.
        """
        # TODO: Implement this.


common_app_handler = CommonAppHandler()
