from selenium.webdriver.support.ui import WebDriverWait
from tools.webkit import BrowserSession
from login import login_livetse
from bs4 import BeautifulSoup
from time import sleep


class LivetseNotificationScraper:
    def __init__(
        self,
        wait_timeout: float = 20,
    ):
        """
        Initializes a browser session and logs in to the Livetse notification page.

        Args:
            wait_timeout (float): Timeout for WebDriverWait. Defaults to 20 seconds.
        """
        url = "https://app.livetse.ir/notification?mode=export_html"
        self.session = BrowserSession(url)
        self.driver = self.session.driver
        self.wait = WebDriverWait(self.driver, wait_timeout)
        self.css_selector = (
            "div.overflow-auto.scrollbar.scrollbar-primary.texual_view.card-body"
        )

        login_livetse(self.driver)
        self._select_all_filters()

    def _select_all_filters(self) -> None:
        """
        Repeatedly clicks the "select all" button until all filters are active.
        """
        locator = "span.select_deselect_all.select"
        button = self.session.eletools.click("CSS_SELECTOR", locator)
        for _ in range(3):
            button.click()
            sleep(3)
            if button.get_attribute("title") == "فعال سازی همه فیلترها":
                break

    def _click_and_wait(self, button_id: str, from_class: str, to_class: str) -> None:
        """
        Clicks a filter button and waits for its class attribute to change.

        Args:
            button_id (str): The ID of the filter button.
            from_class (str): The initial class to wait for removal.
            to_class (str): The target class to wait for.
        """
        element = self.session.eletools.click("ID", button_id)
        self.session.eletools.wait_attr_change(element, from_class, to_class)

    def _get_clean_html(self, report_title: str) -> str:
        """
        Retrieves and cleans the HTML content based on the report type.

        Args:
            report_title (str): The type of report being generated.

        Returns:
            str: The cleaned HTML string.
        """
        raw_html = self.session.eletools.get_content("CSS_SELECTOR", self.css_selector)
        return self._clean_html(raw_html, report_title)

    def _clean_html(self, raw_html: str, report_title: str) -> str:
        """
        Converts raw HTML entities, removes specific tags, and replaces dynamic content.

        Args:
            raw_html (str): The raw HTML content.
            report_title (str): The report type identifier.

        Returns:
            str: Processed and cleaned HTML content.
        """
        raw_html = (
            raw_html.replace("&lt;", "<")
            .replace("&gt;", ">")
            .replace("&amp;", "&")
            .replace("amp;", "")
        )

        html_soup = BeautifulSoup(raw_html, "html.parser")

        for tag in html_soup.select(self.css_selector):
            tag.unwrap()

        if report_title == "livetse_market_report":
            return str(html_soup).replace("6 اردیبهشت 1402", "{{ pretty_jdate }}")

        ul = html_soup.find("ul")
        if not ul:
            return ""

        result_soup = BeautifulSoup("", "html.parser")
        for li in ul.find_all("li"):
            result_soup.append(li.get_text())
            result_soup.append(result_soup.new_tag("br"))

        return str(result_soup)

    def get_market_report(self) -> str:
        """
        Generates the market report by interacting with POSTMARKET filter.

        Returns:
            str: Cleaned HTML of the market report.
        """
        self._click_and_wait("POSTMARKET", "red", "standard")
        return self._get_clean_html("livetse_market_report")

    def get_golden_notification_report(self) -> str:
        """
        Generates the golden notification report by activating multiple filters.

        Returns:
            str: Cleaned HTML of the golden notification report.
        """
        for button in ["UP_TREND", "NAVASAN", "TABLO_MOVEMENT"]:
            self._click_and_wait(button, "red", "gold")
        return self._get_clean_html("livetse_golden_notification_report")

    def close(self) -> None:
        """
        Closes the browser session.
        """
        self.driver.quit()
