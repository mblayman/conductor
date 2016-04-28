from lxml import etree

from planner.scrapers.base import Scraper


class UVAScraper(Scraper):
    """Scraper for the University of Virginia"""

    def scrape(self):
        with open('/home/matt/conductor/uva.html', 'r') as f:
            text = f.read()

        html = etree.HTML(text)

        # Filter to a closer div to prevent extracting too much data.
        div_list = html.xpath('.//div[contains(@class, "view-events")]')
        if len(div_list) != 1:
            raise Exception('Expected 1 div, found {}'.format(len(div_list)))

        events_div = div_list[0]
        for row in events_div.xpath('//tr'):
            print('text', row)
        # TODO: Get list of objects that has raw dates and text
        # TODO: match text against regular expressions to find milestone types
        # TODO: create or update milestones.
        # TODO: Add concept of academic year to milestones?
        # TODO: Refactor to template pattern to reduce mechanical work needed.
