from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from login import login_livetse
from time import sleep
from typing import Literal
from bs4 import BeautifulSoup
import os


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


def save_file(
    content: str,
    path: str = ".",
) -> None:
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def setup_driver():
    """Set up the Selenium WebDriver."""
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver


def click_by_element(
    wait: WebDriverWait,
    by_type: ByType,
    locator: str,
) -> WebElement:
    by = getattr(By, by_type)
    element = wait.until(EC.element_to_be_clickable((by, locator)))
    element.click()
    return element


def wait_element_change(
    wait: WebDriverWait,
    element: WebElement,
    from_value: str,
    to_value: str,
    from_attr: AttrName = "class",
    to_attr: AttrName = "class",
) -> None:
    wait.until(
        lambda name_must_exist: from_value not in element.get_attribute(from_attr)
        and to_value in element.get_attribute(to_attr)
    )


def get_element_content(
    wait: WebDriverWait,
    by_type: ByType,
    locator: str,
) -> str:
    by = getattr(By, by_type)
    content = wait.until(EC.presence_of_element_located((by, locator)))
    raw_html = content.get_attribute("outerHTML")
    return raw_html


def is_file_empty(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} not found.")
    return os.stat(file_path).st_size == 0


def livetse_setup_notification_page():
    driver = setup_driver()
    driver.get("https://app.livetse.ir/notification?mode=export_html")

    login_livetse(driver)

    wait = WebDriverWait(driver, 20)

    # Click the "select all" button
    select_all_button = wait.until(
        EC.element_to_be_clickable((By.CSS_SELECTOR, "span.select_deselect_all.select"))
    )
    for _ in range(3):
        select_all_button.click()
        sleep(3)
        if select_all_button.get_attribute("title") == "فعال سازی همه فیلترها":
            break

    return driver


def livetse_clean_html(raw_html, report_title, css_selector):
    raw_html = (
        raw_html.replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("amp;amp;", "")
        .replace("&amp;", "&")
    )

    html_soup = BeautifulSoup(raw_html, "html.parser")

    for tag in html_soup.select(css_selector):
        tag.unwrap()

    if report_title == "market_report":
        return str(html_soup)

    ul = html_soup.find("ul")
    if not ul:
        return ""

    # Extract text from li and add br
    result_soup = BeautifulSoup("", "html.parser")
    for li in ul.find_all("li"):
        result_soup.append(li.get_text())
        result_soup.append(result_soup.new_tag("br"))

    return str(result_soup)


def livetse_market_report():
    driver = livetse_setup_notification_page()
    wait = WebDriverWait(driver, 20)

    # Click the POSTMARKET button and wait for class change to green
    element = click_by_element(wait, "ID", "POSTMARKET")
    wait_element_change(wait, element, "red", "standard")

    # Get the HTML content and save it
    css_selector = "div.overflow-auto.scrollbar.scrollbar-primary.texual_view.card-body"
    raw_html = get_element_content(wait, "CSS_SELECTOR", css_selector)

    sleep(1)
    driver.quit()

    data = livetse_clean_html(raw_html, "market_report", css_selector)
    save_file(data, "templates/market_report.html")


def livetse_golden_notification_report():
    driver = livetse_setup_notification_page()
    wait = WebDriverWait(driver, 20)

    # Click the UP_TREND, NAVASAN and TABLO_MOVEMENT buttons and wait for classes change to gold
    buttons = ["UP_TREND", "NAVASAN", "TABLO_MOVEMENT"]
    for button in buttons:
        element = click_by_element(wait, "ID", button)
        wait_element_change(wait, element, "red", "gold")

    css_selector = "div.overflow-auto.scrollbar.scrollbar-primary.texual_view.card-body"
    raw_html = get_element_content(wait, "CSS_SELECTOR", css_selector)

    sleep(1)
    driver.quit()

    data = livetse_clean_html(raw_html, "golden_notification_report", css_selector)
    save_file(data, "templates/golden_notification_report.html")


def main():
    livetse_market_report()
    print("Market report has been successfully saved.")

    livetse_golden_notification_report()
    print("Golden notification report has been successfully saved.")


if __name__ == "__main__":
    main()
