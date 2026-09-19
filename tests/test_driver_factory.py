import unittest
from unittest.mock import patch

from scraper.driver_factory import ChromeDriverFactory, _detect_chromedriver_binary


class ChromeDriverFactoryTests(unittest.TestCase):
    @patch("scraper.driver_factory.os.path.isfile")
    def test_detect_chromedriver_binary_prefers_environment_path(self, isfile):
        env_path = "/tmp/custom/chromedriver"

        def fake_isfile(path):
            return path == env_path

        isfile.side_effect = fake_isfile

        with patch.dict("scraper.driver_factory.os.environ", {"CHROMEDRIVER_PATH": env_path}, clear=True):
            self.assertEqual(_detect_chromedriver_binary(), env_path)

    @patch("scraper.driver_factory.webdriver.Chrome")
    def test_create_uses_explicit_service_for_local_driver(self, chrome):
        factory = ChromeDriverFactory(
            binary_location="/usr/bin/google-chrome",
            driver_path="/usr/local/bin/chromedriver",
        )

        factory.create()

        _, kwargs = chrome.call_args
        self.assertEqual(kwargs["service"].path, "/usr/local/bin/chromedriver")
        self.assertEqual(kwargs["options"].binary_location, "/usr/bin/google-chrome")

    @patch("scraper.driver_factory.webdriver.Chrome")
    def test_create_falls_back_when_local_driver_is_unavailable(self, chrome):
        factory = ChromeDriverFactory(
            binary_location="/usr/bin/google-chrome",
            driver_path=None,
        )

        factory.create()

        _, kwargs = chrome.call_args
        self.assertIsNone(kwargs["service"])
        self.assertEqual(kwargs["options"].binary_location, "/usr/bin/google-chrome")

    @patch("scraper.driver_factory.os.path.isfile")
    def test_detect_chromedriver_binary_uses_default_local_path(self, isfile):
        def fake_isfile(path):
            return path == "/usr/local/bin/chromedriver"

        isfile.side_effect = fake_isfile

        with patch.dict("scraper.driver_factory.os.environ", {}, clear=True):
            self.assertEqual(_detect_chromedriver_binary(), "/usr/local/bin/chromedriver")


if __name__ == "__main__":
    unittest.main()
