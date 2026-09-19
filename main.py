"""Entry point: scrape https://squidfunk.github.io/mkdocs-material/ with Selenium."""
import json

from scraper import MkDocsMaterialScraper

TARGET_URL = "https://squidfunk.github.io/mkdocs-material/"


def main() -> None:
    with MkDocsMaterialScraper(base_url=TARGET_URL) as scraper:
        summary = scraper.run()

    print(f"Title: {summary.title}")
    print(f"Tagline: {summary.tagline}")

    print(f"\nTop navigation tabs ({len(summary.tabs)}):")
    for tab in summary.tabs:
        print(f"  - {tab.text}: {tab.url}")

    print(f"\nSidebar navigation links ({len(summary.navigation)}):")
    for link in summary.navigation[:15]:
        print(f"  - {link.text}: {link.url}")

    print("\nFull summary (JSON):")
    print(json.dumps(summary.to_dict(), indent=2))


if __name__ == "__main__":
    main()
