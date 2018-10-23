import time
from typing import List

from bs4 import BeautifulSoup
import requests

from conductor import celeryapp
from conductor.trackers.handlers import common_app_handler
from conductor.trackers.models import RawCommonAppSchool


@celeryapp.task
def scan_common_app_schools() -> None:
    """Scan the Common App site for the member schools."""
    common_app_domain = "https://www.commonapp.org"
    common_app_url = f"{common_app_domain}/search-colleges"

    common_app_schools: List[RawCommonAppSchool] = []

    while True:
        response = requests.get(common_app_url, timeout=5)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        schools = soup.find_all("div", "school-content-wrapper")
        for school in schools:
            school_url = school.h2.a.get("href")
            slug = school_url.split("/")[-1]
            common_app_schools.append(
                RawCommonAppSchool(name=school.h2.a.string, slug=slug)
            )

        pager_next = soup.find_all("li", "pager-next")
        if pager_next:
            next_url = pager_next[0].a.get("href")
            common_app_url = f"{common_app_domain}{next_url}"
            time.sleep(5)  # Don't hammer the servers.
        else:
            break

    common_app_handler.handle(common_app_schools)
