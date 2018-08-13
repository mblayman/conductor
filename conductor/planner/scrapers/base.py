class Scraper(object):
    """Scrape a milestones page to find a school's important dates."""

    def scrape(self) -> None:
        """Scape a page for milestone dates.

        Create or update school milestones.
        """
        raise NotImplementedError()
