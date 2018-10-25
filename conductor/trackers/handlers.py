from typing import List

from conductor.trackers.models import CommonAppTracker, RawCommonAppSchool


class CommonAppHandler:
    """Process the common app schools that were fetched from the website."""

    def handle(self, common_app_schools: List[RawCommonAppSchool]) -> None:
        """Handle each school to add to tracking if needed."""
        active_tracked_school_count = CommonAppTracker.objects.exclude(
            status=CommonAppTracker.REMOVED
        ).count()
        # Assume that if the count matches, then the database is current.
        if len(common_app_schools) == active_tracked_school_count:
            return

        if active_tracked_school_count > len(common_app_schools):
            common_app_school_slugs = [
                raw_common_app_school.slug
                for raw_common_app_school in common_app_schools
            ]
            newly_removed_trackers = CommonAppTracker.objects.exclude(
                status=CommonAppTracker.REMOVED
            )
            newly_removed_trackers = newly_removed_trackers.exclude(
                slug__in=common_app_school_slugs
            )
            # TODO: Report any schools that should be REMOVED.

        for raw_common_app_school in common_app_schools:
            self.process_school(raw_common_app_school)

    def process_school(self, raw_common_app_school: RawCommonAppSchool) -> None:
        """Process the raw school into a tracked school.

        Track the add/mod/delete status compared to the database.
        """
        try:
            common_app_tracker = CommonAppTracker.objects.get(
                slug=raw_common_app_school.slug
            )
            common_app_tracker.name = raw_common_app_school.name
            common_app_tracker.save()
        except CommonAppTracker.DoesNotExist:
            CommonAppTracker.objects.create(
                name=raw_common_app_school.name, slug=raw_common_app_school.slug
            )


common_app_handler = CommonAppHandler()
