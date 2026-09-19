"""Factory for creating configured Selenium Chrome WebDriver instances."""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Optional, Tuple

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service


def _detect_chrome_binary() -> Optional[str]:
    """Locates a usable Chrome/Chromium binary across common install paths."""
    candidates = (
        os.environ.get("CHROME_BINARY_PATH"),
        "/usr/bin/google-chrome",
        "/usr/bin/chromium",
        "/opt/pw-browsers/chromium-1194/chrome-linux/chrome",
    )
    for candidate in candidates:
        if candidate and os.path.isfile(candidate):
            return candidate
    return None


def _detect_chromedriver_binary() -> Optional[str]:
    """Locates a usable ChromeDriver binary across common install paths."""
    candidates = (
        os.environ.get("CHROMEDRIVER_PATH"),
        "/usr/local/bin/chromedriver",
        "/usr/bin/chromedriver",
    )
    for candidate in candidates:
        if candidate and os.path.isfile(candidate):
            return candidate
    return None


@dataclass
class ChromeDriverFactory:
    """Builds headless Chrome WebDriver instances with sane, shared defaults.

    Centralising driver construction here means every scraper reuses the
    same options/preferences setup instead of re-declaring it per-class.
    """

    headless: bool = True
    window_size: Tuple[int, int] = (1920, 1080)
    binary_location: Optional[str] = field(default_factory=_detect_chrome_binary)
    driver_path: Optional[str] = field(default_factory=_detect_chromedriver_binary)
    disable_images: bool = True

    def build_options(self) -> Options:
        options = Options()
        if self.binary_location:
            options.binary_location = self.binary_location
        if self.headless:
            options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument(f"--window-size={self.window_size[0]},{self.window_size[1]}")
        if self.disable_images:
            options.add_experimental_option(
                "prefs", {"profile.default_content_settings": {"images": 2}}
            )
        return options

    def create(self) -> webdriver.Chrome:
        service = Service(executable_path=self.driver_path) if self.driver_path else None
        return webdriver.Chrome(options=self.build_options(), service=service)
