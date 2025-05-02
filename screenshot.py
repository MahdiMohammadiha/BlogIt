from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import os


def take_screenshot(url, selector, output_path):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=options)
    driver.get(url)

    try:
        wait = WebDriverWait(driver, 10)
        element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        if element.is_displayed():
            element.screenshot(output_path)
            print("Screenshot saved.")
            success = True
        else:
            print("Element not visible.")
            success = False

    except Exception as e:
        print("Error:", e)
        success = False

    driver.quit()
    return success
