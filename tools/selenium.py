from atexit import register
from selenium import webdriver
from selenium.webdriver.chrome.webdriver import WebDriver
from typing import Literal


# Allowed types for By
ByType = Literal[
    "ID",
    "XPATH",
    "CSS_SELECTOR",
    "NAME",
    "TAG_NAME",
    "CLASS_NAME",
    "LINK_TEXT",
    "PARTIAL_LINK_TEXT",
]

# Allowed names for attribute
AttrName = Literal[
    "class",
    "id",
    "name",
    "value",
    "type",
    "href",
    "src",
    "alt",
    "title",
    "placeholder",
    "disabled",
    "checked",
    "selected",
]


def setup_driver(
    url: str = "", 
    headless: bool = True, 
    window_size: list[int] | None = None
) -> WebDriver:
    """
    Initializes and returns a Chrome WebDriver with specified options.
    The driver will be automatically quit when the program exits.

    Args:
        url (str): The URL to open after initializing the driver. Defaults to an empty string.
        headless (bool): If True, runs the browser in headless mode. Defaults to True.
        window_size (list[int] | None): The window size [width, height] used in headless mode.
            Defaults to [1366, 768] if not provided.

    Returns:
        WebDriver: An instance of Chrome WebDriver with the given configuration.
    """
    if window_size is None:
        window_size = [1366, 768]

    options = webdriver.ChromeOptions()
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")

    if headless:
        options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)

    if headless:
        driver.set_window_size(window_size[0], window_size[1])
    else:
        driver.maximize_window()

    driver.get(url)

    # Register auto-quit at program exit
    register(driver.quit)

    return driver
