"""Site-specific scraper for the Material for MkDocs documentation site."""
from __future__ import annotations

from urllib.parse import urljoin

from selenium.webdriver.common.by import By

from .base_scraper import BaseScraper, Locator
from .models import NavLink, SiteSummary


class MkDocsMaterialScraper(BaseScraper[SiteSummary]):
    """Extracts the title, tagline, top tabs and side navigation from
    https://squidfunk.github.io/mkdocs-material/.
    """

    TAB_LOCATOR: Locator = (By.CSS_SELECTOR, ".md-tabs__link")
    NAV_LOCATOR: Locator = (By.CSS_SELECTOR, ".md-nav--primary .md-nav__link")
    TAGLINE_LOCATOR: Locator = (By.CSS_SELECTOR, ".md-typeset > p")

    def scrape(self) -> SiteSummary:
        return SiteSummary(
            url=self.driver.current_url,
            title=self.driver.title,
            tagline=self._first_tagline(),
            tabs=self._extract_links(self.TAB_LOCATOR),
            navigation=self._extract_links(self.NAV_LOCATOR),
        )

    def _first_tagline(self) -> str:
        elements = self.find_all(self.TAGLINE_LOCATOR)
        return self.text_of(elements[0]) if elements else ""

    def _extract_links(self, locator: Locator) -> list[NavLink]:
        """Shared dedup/normalise logic for both the top tabs and the sidebar."""
        links: list[NavLink] = []
        seen: set[str] = set()
        for element in self.find_all(locator):
            text = self.text_of(element)
            href = self.attr_of(element, "href")
            if not text or not href or href in seen:
                continue
            seen.add(href)
            links.append(NavLink(text=text, url=urljoin(self.driver.current_url, href)))
        return links
