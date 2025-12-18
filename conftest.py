import pytest

from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        action="store",
        default="chrome",
        choices=("chrome", "firefox"),
        help="Browser for UI tests: chrome or firefox",
    )


@pytest.fixture
def driver(request):
    browser = request.config.getoption("browser")

    if browser == "chrome":
        options = ChromeOptions()
        options.add_argument("--start-maximized")
        drv = webdriver.Chrome(options=options)
    elif browser == "firefox":
        options = FirefoxOptions()
        drv = webdriver.Firefox(options=options)
        drv.maximize_window()
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    yield drv
    drv.quit()
