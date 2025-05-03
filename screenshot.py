from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


def __print_comment(comment):
    print("screenshot.py =>", comment)


def take_screenshot(url, selector, output_path, index=1, timeout=10):
    try:
        index = int(index)
        timeout = int(timeout)
    except ValueError:
        comment = "Invalid inputs."
        __print_comment(comment)
        return False, comment

    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 10)
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
            element.screenshot(output_path)
            comment = "Screenshot saved."
            success = True
        else:
            comment = "Element not visible."
            success = False

    except Exception as e:
        comment = "An error occurred."
        __print_comment(f"Exception occurred: {type(e).__name__}.")
        success = False

    finally:
        driver.quit()
        __print_comment(comment)

    return success, comment
