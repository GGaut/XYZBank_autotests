from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.settings import settings


class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, settings.WAIT_TIMER)

    def open_url(self, url: str):
        self.driver.get(url)
        return self

    def wait_for_element(self, locator):
        self.wait.until(EC.presence_of_element_located(locator))

    def find_element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))

    def click_element(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
        return self

    def enter_text(self, locator, text: str):
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)
        return self

    def get_text(self, locator) -> str:
        element = self.find_element(locator)
        return element.text

    def is_element_present(self, locator) -> bool:
        try:
            self.find_element(locator)
            return True
        except (NoSuchElementException, TimeoutException):
            return False
