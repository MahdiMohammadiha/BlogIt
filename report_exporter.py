from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login import login_livetse
from time import sleep


def setup_driver():
    """Set up the Selenium WebDriver."""
    options = webdriver.ChromeOptions()
    # options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.maximize_window()
    return driver


def livetse_market_report(driver):
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

    # Click the POSTMARKET button and wait for class change
    post_market_button = wait.until(EC.element_to_be_clickable((By.ID, "POSTMARKET")))
    post_market_button.click()
    wait.until(
        lambda d: "standard" in post_market_button.get_attribute("class")
        and "red" not in post_market_button.get_attribute("class")
    )

    # Get the HTML content and save it
    element = wait.until(
        EC.presence_of_element_located(
            (
                By.CSS_SELECTOR,
                "div.overflow-auto.scrollbar.scrollbar-primary.texual_view.card-body",
            )
        )
    )

    parrent_element = (
        '<div class="overflow-auto scrollbar scrollbar-primary texual_view card-body">'
    )

    raw_html = element.get_attribute("outerHTML")
    clean_html = (
        raw_html.replace(parrent_element, "")
        .replace("&lt;", "<")
        .replace("&gt;", ">")
        .replace("amp;amp;", "")
    )

    with open("market_report.html", "w", encoding="utf-8") as f:
        f.write(clean_html)


def main():
    driver = setup_driver()

    try:
        livetse_market_report(driver)
        print("Market report has been successfully saved.")

    finally:
        driver.quit()


if __name__ == "__main__":
    main()
