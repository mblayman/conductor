from conductor.tests import TestCase
from planner.scrapers.base import Scraper


class TestScraper(TestCase):

    def test_scrape_not_implemented(self):
        scraper = Scraper()
        self.assertRaises(NotImplementedError, scraper.scrape)
