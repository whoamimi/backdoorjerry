"""Plain data containers for scraped Material for MkDocs content."""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class NavLink:
    text: str
    url: str


@dataclass
class SiteSummary:
    url: str
    title: str
    tagline: str
    tabs: List[NavLink] = field(default_factory=list)
    navigation: List[NavLink] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "title": self.title,
            "tagline": self.tagline,
            "tabs": [link.__dict__ for link in self.tabs],
            "navigation": [link.__dict__ for link in self.navigation],
        }
