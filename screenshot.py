import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from login import login_livetse as LL
from logger import print_console as PC
from time import sleep
from contextlib import closing


FILE_NAME = os.path.basename(__file__)


def valid_inputs(
    url, selector, output_paths, indexes, timeout, login_required, pre_actions
):
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

    if not isinstance(pre_actions, list):
        PC(FILE_NAME, "Pre action must be a list.")
        return False

    if not isinstance(login_required, bool):
        PC(FILE_NAME, "Login must be a boolean.")
        return False

    return True


def save_screenshot(element, path):
    element.screenshot(path)
    return True, "Screenshot saved."


def perform_pre_actions(driver, pre_actions, timeout=10):
    wait = WebDriverWait(driver, timeout)
    for action in pre_actions:
        try:
            if action["type"] == "select":
                select_element = wait.until(
                    EC.presence_of_element_located((By.ID, action["select_id"]))
                )
                select_obj = Select(select_element)
                select_obj.select_by_visible_text(action["option_text"])
                sleep(1)
        except Exception as e:
            PC(FILE_NAME, f"Pre-action failed: {type(e).__name__}.")


def capture_element(
    driver,
    selector,
    output_path,
    index,
    timeout,
    delay,
    scroll_into_view,
    is_first_screenshot,
):
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
            if scroll_into_view:
                driver.execute_script(
                    "arguments[0].scrollIntoView({block: 'center'});", element
                )

            if is_first_screenshot:
                sleep(delay)
            else:
                sleep(0.5)  # Give it time to stabilize

            success, message = save_screenshot(element, output_path)

        else:
            message = "Element not visible."
            success = False

    except Exception as e:
        message = f"Exception occurred: {type(e).__name__}."
        success = False

    return success, message


def setup_deriver(url, window_size=[1366, 768]):
    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--log-level=3")
    driver = webdriver.Chrome(options=options)

    if "--headless" in options.arguments:
        driver.set_window_size(window_size[0], window_size[1])
    else:
        driver.maximize_window()

    driver.get(url)
    driver.execute_script("document.body.style.zoom='100%'")
    return driver


def take_screenshot(
    url: str,
    selector: str,
    output_paths: list[str],
    indexes: list[int] = [1],
    timeout: int = 10,
    delay: int = 1,
    login_required: bool = False,
    scroll_into_view: bool = False,
    pre_actions: list[dict] = [],
    window_size: list[int, int] = [1366, 768],
) -> list[tuple[bool, str]]:

    if not valid_inputs(
        url, selector, output_paths, indexes, timeout, login_required, pre_actions
    ):
        return [(False, "Invalid inputs.")]

    with closing(setup_deriver(url, window_size)) as driver:
        if login_required:
            LL(driver)

        if pre_actions:
            perform_pre_actions(driver, pre_actions, timeout)

        results = []
        is_first_screenshot = True

        for index, output_path in zip(indexes, output_paths):
            success, message = capture_element(
                driver=driver,
                selector=selector,
                output_path=output_path,
                index=index,
                timeout=timeout,
                delay=delay,
                scroll_into_view=scroll_into_view,
                is_first_screenshot=is_first_screenshot,
            )
            is_first_screenshot = False
            PC(FILE_NAME, message)
            results.append((success, message))

    return results


if __name__ == "__main__":
    print(FILE_NAME)
