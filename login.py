from os import getenv
from dotenv import load_dotenv
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from logger import print_console as PC


def login_livetse(driver):
    """
    Note:
        If __pycache__ files are generated and this file is imported from another module
        without the `if __name__ == "__main__"` guard, and the PHONE_NUMBER or PASSWORD
        values have been changed in the .env file, cached values might be used instead.
        This can lead to using outdated credentials.
        To ensure the .env values are always up-to-date, use `load_dotenv()` inside functions
        or protect direct execution with `if __name__ == "__main__"`.
    """
    load_dotenv()
    phone_number = getenv("PHONE_NUMBER")
    password = getenv("PASSWORD")

    wait = WebDriverWait(driver, 20)

    phone_input = wait.until(EC.presence_of_element_located((By.TAG_NAME, "input")))
    phone_input.send_keys(phone_number)
    phone_input.send_keys(Keys.ENTER)

    password_input = wait.until(EC.presence_of_element_located((By.NAME, "password")))
    password_input.send_keys(password)
    password_input.send_keys(Keys.ENTER)


if __name__ == "__main__":
    load_dotenv()
    phone_number = getenv("PHONE_NUMBER")
    password = getenv("PASSWORD")

    print(phone_number, password)
