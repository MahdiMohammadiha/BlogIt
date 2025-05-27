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
from jdatetime import date
import json
import htmlmin


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


def save_file_j(data, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def save_file(
    data: str,
    path: str = ".",
) -> None:
    data = str(data)
    with open(path, "w", encoding="utf-8") as f:
        f.write(data)


def jalali_date():
    today = date.today()
    jalali_date = today.strftime("%d %B %Y")

    return str(jalali_date)


def minify_html(input_path: str, output_path: str = ""):
    if not output_path:
        output_path = input_path
    
    with open(input_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    minified_html = htmlmin.minify(html_content, remove_comments=True, remove_empty_space=True)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(minified_html)


def setup_driver(url="", window_size=[1366, 768]):
    """Set up the Selenium WebDriver."""
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)

    if "--headless" in options.arguments:
        driver.set_window_size(window_size[0], window_size[1])
    else:
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


def tsetmc_index_report():
    """
    Debloat required!
    """

    # Launch the browser
    driver = setup_driver()
    driver.get("https://old.tsetmc.com/Loader.aspx?ParTree=15")

    # Wait until the index tables are loaded
    wait = WebDriverWait(driver, 15)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "table1")))

    # Find all tables with class 'table1'
    tables = driver.find_elements(By.CLASS_NAME, "table1")

    # The second table contains the selected indices
    target_table = tables[1]

    # Get all table rows
    rows = target_table.find_elements(By.TAG_NAME, "tr")

    # Prepare the result dictionary
    result = {}

    # Mapping from Persian names to English keys
    index_map = {
        "شاخص كل": "overall_index",
        "شاخص كل (هم وزن)": "equal_weight_index",
        "شاخص قيمت (هم وزن)": "equal_weight_price",
    }

    # Loop through rows and extract values
    for row in rows[1:]:
        cols = row.find_elements(By.TAG_NAME, "td")

        if not cols:
            continue

        name = cols[0].text.strip()
        if name in index_map:
            key = index_map[name]
            value = cols[2].text.strip()
            change_td = cols[3]
            change = change_td.text.strip()
            percent = cols[4].text.strip()

            # Check if the change is positive or negative based on class
            inner_div = change_td.find_element(By.TAG_NAME, "div")
            change_class = inner_div.get_attribute("class")
            is_positive = "pn" in change_class  # true if positive

            result[key] = {
                "value": value,
                "change": change,
                "percent": percent,
                "is_positive": is_positive,
            }

    # Close the browser
    driver.quit()

    save_file_j(result, "templates/reports/tsetmc_index_report.json")
    return result


def livetse_setup_notification_page():
    driver = setup_driver()
    driver.get("https://app.livetse.ir/notification?mode=export_html")

    login_livetse(driver)

    wait = WebDriverWait(driver, 20)

    # Click the "select all" button
    select_all_button = click_by_element(
        wait, "CSS_SELECTOR", "span.select_deselect_all.select"
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
        .replace("&amp;", "&")
        .replace("amp;", "")
    )

    html_soup = BeautifulSoup(raw_html, "html.parser")

    for tag in html_soup.select(css_selector):
        tag.unwrap()

    if report_title == "livetse_market_report":
        html_soup = str(html_soup).replace("6 اردیبهشت 1402", "{{ jalali_date }}")
        return html_soup

    ul = html_soup.find("ul")
    if not ul:
        return ""

    # Extract text from li and add br
    result_soup = BeautifulSoup("", "html.parser")
    for li in ul.find_all("li"):
        result_soup.append(li.get_text())
        result_soup.append(result_soup.new_tag("br"))

    return result_soup


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

    data = livetse_clean_html(raw_html, "livetse_market_report", css_selector)
    save_file(data, "templates/reports/livetse_market_report.html")


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

    data = livetse_clean_html(
        raw_html, "livetse_golden_notification_report", css_selector
    )
    save_file(data, "templates/reports/livetse_golden_notification_report.html")


def main():
    livetse_market_report()
    print("Market report has been successfully saved.")

    livetse_golden_notification_report()
    print("Golden notification report has been successfully saved.")

    tsetmc_index_report()
    print("TSETMC index report has been successfully saved.")


if __name__ == "__main__":
    main()
