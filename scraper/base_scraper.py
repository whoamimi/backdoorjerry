"""Template-method base class shared by all site-specific scrapers."""
from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Generic, List, Optional, Tuple, TypeVar

from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .driver_factory import ChromeDriverFactory

Locator = Tuple[str, str]
T = TypeVar("T")


class BaseScraper(ABC, Generic[T]):
    """Owns the Selenium driver lifecycle and common element-access helpers.

    Subclasses only implement `scrape()`; waiting, safe text/attribute
    extraction and page loading are handled once here so concrete scrapers
    don't reimplement the same boilerplate.
    """

    default_timeout: float = 10

    def __init__(self, base_url: str, driver_factory: Optional[ChromeDriverFactory] = None):
        self.base_url = base_url
        self._driver_factory = driver_factory or ChromeDriverFactory()
        self.driver: Optional[WebDriver] = None

    def __enter__(self) -> "BaseScraper[T]":
        self.driver = self._driver_factory.create()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        if self.driver is not None:
            self.driver.quit()
            self.driver = None

    def run(self, path: str = "") -> T:
        """Opens the target page and delegates extraction to `scrape()`."""
        if self.driver is None:
            raise RuntimeError(f"{type(self).__name__} must be used as a context manager")
        self.load(path)
        return self.scrape()

    def load(self, path: str = "") -> None:
        url = self.base_url if not path else f"{self.base_url.rstrip('/')}/{path.lstrip('/')}"
        self.driver.get(url)
        self.wait_for((By.TAG_NAME, "body"))

    @abstractmethod
    def scrape(self) -> T:
        """Extracts and returns structured data from the currently loaded page."""

    def wait_for(self, locator: Locator, timeout: Optional[float] = None) -> WebElement:
        wait = WebDriverWait(self.driver, timeout or self.default_timeout)
        return wait.until(EC.presence_of_element_located(locator))

    def find_all(self, locator: Locator) -> List[WebElement]:
        return self.driver.find_elements(*locator)

    @staticmethod
    def text_of(element: Optional[WebElement], default: str = "") -> str:
        if element is None:
            return default
        return element.text.strip() or default

    @staticmethod
    def attr_of(element: Optional[WebElement], name: str, default: str = "") -> str:
        if element is None:
            return default
        value = element.get_attribute(name)
        return value.strip() if value else default
