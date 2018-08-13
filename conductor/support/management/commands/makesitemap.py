import os
from typing import Any
from xml.etree.ElementTree import Element, ElementTree, SubElement

from django.conf import settings
from django.core.management.base import BaseCommand
from django.urls import reverse

from conductor.planner.models import School


class Command(BaseCommand):
    help = "Make a sitemap.xml"

    def handle(self, *args: Any, **options: Any) -> None:
        """Build a sitemap.xml and output it to the templates directory."""
        sitemap = Element(
            "urlset", attrib={"xmlns": "http://www.sitemaps.org/schemas/sitemap/0.9"}
        )

        # Core marketing/non-authenticated views
        sitemap.append(self.build_url(reverse("index"), priority=1.0))
        sitemap.append(self.build_url(reverse("signup"), priority=1.0))
        sitemap.append(self.build_url(reverse("contact")))
        sitemap.append(self.build_url(reverse("terms")))
        sitemap.append(self.build_url(reverse("privacy")))

        for school in School.objects.all():
            url = self.build_url(reverse("school-detail", args=[school.slug]))
            sitemap.append(url)

        self.write_sitemap(sitemap)

    def build_url(
        self, path: str, change_frequency: str = "monthly", priority: float = 0.5
    ) -> Element:
        url = Element("url")
        loc = SubElement(url, "loc")
        loc.text = "https://www.collegeconductor.com" + path
        changefreq = SubElement(url, "changefreq")
        changefreq.text = change_frequency
        priority_node = SubElement(url, "priority")
        priority_node.text = str(priority)
        return url

    def write_sitemap(self, sitemap: Element) -> None:
        sitemap_path = os.path.join(
            settings.ROOT_DIR, "conductor", "templates", "sitemap.xml"
        )
        ElementTree(sitemap).write(sitemap_path, encoding="UTF-8", xml_declaration=True)
