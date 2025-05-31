from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from tools.filekit import save_file
from tools.webkit import BrowserSession
from tools.livetse import LivetseNotificationScraper as LNS
from tools.utils import JalaliDate


ISO_JDATE = str(JalaliDate().iso())


def tsetmc_index_report():
    """
    Debloat required!
    """

    # Launch the browser
    url = "https://old.tsetmc.com/Loader.aspx?ParTree=15"
    session = BrowserSession(url, True)
    driver = session.driver
    wait = session.wait

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
    session.exit()

    save_file(result, f"templates/reports/{ISO_JDATE}/tsetmc_index_report.json")
    return result


def livetse_market_report() -> None:
    scraper = LNS()
    html = scraper.get_market_report()
    save_file(html, f"templates/reports/{ISO_JDATE}/livetse_market_report.html")
    scraper.close()


def livetse_golden_notification_report() -> None:
    scraper = LNS()
    html = scraper.get_golden_notification_report()
    save_file(html, f"templates/reports/{ISO_JDATE}/livetse_golden_notification_report.html")
    scraper.close()


def main():
    livetse_market_report()
    print("Market report has been successfully saved.")

    livetse_golden_notification_report()
    print("Golden notification report has been successfully saved.")

    tsetmc_index_report()
    print("TSETMC index report has been successfully saved.")


if __name__ == "__main__":
    main()
