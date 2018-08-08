from lxml import etree

from conductor.planner.scrapers.base import Scraper


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
