from typing import Dict, List

from django.conf import settings
from django.core.mail import EmailMessage

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

        stats: Dict[str, List[CommonAppTracker]] = {
            "add": [],
            "modify": [],
            "delete": [],
        }

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
            stats["delete"] = list(newly_removed_trackers)

        for raw_common_app_school in common_app_schools:
            self.process_school(raw_common_app_school, stats)

        self.report(stats)

    def process_school(
        self,
        raw_common_app_school: RawCommonAppSchool,
        stats: Dict[str, List[CommonAppTracker]],
    ) -> None:
        """Process the raw school into a tracked school.

        Track the add/mod/delete status compared to the database.
        """
        try:
            common_app_tracker = CommonAppTracker.objects.get(
                slug=raw_common_app_school.slug
            )
            if common_app_tracker.name != raw_common_app_school.name:
                common_app_tracker.name = raw_common_app_school.name
                common_app_tracker.save()
                stats["modify"].append(common_app_tracker)
        except CommonAppTracker.DoesNotExist:
            common_app_tracker = CommonAppTracker.objects.create(
                name=raw_common_app_school.name, slug=raw_common_app_school.slug
            )
            stats["add"].append(common_app_tracker)

    def report(self, stats: Dict[str, List[CommonAppTracker]]) -> None:
        """Send the email."""
        added_trackers = [
            common_app_tracker.name for common_app_tracker in stats["add"]
        ]
        added = "\n".join(added_trackers)
        modified_trackers = [
            common_app_tracker.name for common_app_tracker in stats["modify"]
        ]
        modified = "\n".join(modified_trackers)
        deleted_trackers = [
            common_app_tracker.name for common_app_tracker in stats["delete"]
        ]
        deleted = "\n".join(deleted_trackers)
        body = f"Add:\n{added}\n\nModify:\n{modified}\n\nDelete:\n{deleted}"
        email = EmailMessage(
            "Common App Schools Processed", body, to=[settings.CONDUCTOR_EMAIL]
        )
        email.send()


common_app_handler = CommonAppHandler()
