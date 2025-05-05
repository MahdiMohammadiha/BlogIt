import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login import login_livetse as LL
from logger import print_console as PC
from time import sleep


FILE_NAME = os.path.basename(__file__)


def take_screenshot(
    url, selector, output_path, index=1, timeout=10, login_required=False
):
    try:
        index = int(index)
        timeout = int(timeout)
    except ValueError:
        comment = "Invalid inputs."
        PC(FILE_NAME, comment)
        return False, comment

    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(2560, 1440)
    driver.get(url)
    driver.execute_script("document.body.style.zoom='100%'")

    wait = WebDriverWait(driver, timeout)

    if login_required:
        LL(driver)

    try:
        elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
        )

        if not elements:
            comment = "No elements found."
            return False, comment

        if index < 1 or index > len(elements):
            comment = f"Index out of range. Found {len(elements)} element(s), but index is {index}."
            return False, comment

        element = elements[index - 1]  # 1-based index

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        if element.is_displayed():
            sleep(10)
            element.screenshot(output_path)
            comment = "Screenshot saved."
            success = True
        else:
            comment = "Element not visible."
            success = False

    except Exception as e:
        comment = "An error occurred."
        PC(FILE_NAME, f"Exception occurred: {type(e).__name__}.")
        success = False

    finally:
        driver.quit()
        PC(FILE_NAME, comment)

    return success, comment
