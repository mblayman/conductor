from conductor.planner.scrapers.base import Scraper
from conductor.tests import TestCase


class TestScraper(TestCase):
    def test_scrape_not_implemented(self) -> None:
        scraper = Scraper()
        self.assertRaises(NotImplementedError, scraper.scrape)
