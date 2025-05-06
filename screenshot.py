import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from login import login_livetse as LL
from logger import print_console as PC
from time import sleep
from contextlib import closing


FILE_NAME = os.path.basename(__file__)


def save_screenshot(element, path):
    element.screenshot(path)
    return True, "Screenshot saved."


def valid_inputs(url, selector, output_paths, indexes, timeout, login_required):
    try:
        timeout = int(timeout)
    except ValueError:
        PC(FILE_NAME, "Timeout must be an integer.")
        return False

    if len(output_paths) != len(indexes):
        PC(FILE_NAME, "The number of output paths must match the number of indexes.")
        return False

    if not url or not selector:
        PC(FILE_NAME, "URL and selector cannot be empty.")
        return False

    return True


def capture_element(driver, selector, output_path, index, timeout):
    wait = WebDriverWait(driver, timeout)

    try:
        elements = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
        )

        if not elements:
            message = "No elements found."
            return False, message

        if index < 1 or index > len(elements):
            message = f"Index out of range. Found {len(elements)} element(s), but index is {index}."
            return False, message

        element = elements[index - 1]  # 1-based index

        os.makedirs(os.path.dirname(output_path), exist_ok=True)  # check & create path

        if element.is_displayed():
            sleep(10)
            success, message = save_screenshot(element, output_path)
        else:
            message = "Element not visible."
            success = False

    except Exception as e:
        message = f"Exception occurred: {type(e).__name__}."
        success = False

    return success, message


def setup_driver():
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    return webdriver.Chrome(options=options)


def take_screenshot(
    url: str,
    selector: str,
    output_paths: list[str],
    indexes: list[int] = [1],
    timeout: int = 10,
    login_required: bool = False,
) -> list[tuple[bool, str]]:

    if not valid_inputs(url, selector, output_paths, indexes, timeout, login_required):
        return [(False, "Invalid inputs.")]

    with closing(setup_driver()) as driver:
        driver.set_window_size(2560, 1440)
        driver.get(url)
        driver.execute_script("document.body.style.zoom='100%'")

        if login_required:
            LL(driver)

        results = []

        for index, output_path in zip(indexes, output_paths):
            success, message = capture_element(
                driver, selector, output_path, index, timeout
            )
            PC(FILE_NAME, message)
            results.append((success, message))

    return results


if __name__ == "__main__":
    pass
