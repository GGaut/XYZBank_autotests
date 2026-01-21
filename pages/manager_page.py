import allure
from selenium.common.exceptions import NoAlertPresentException

from config.settings import settings
from pages.base_page import BasePage
from pages.locators import ManagerPageLocators
from utils.data_generator import find_closest_name_to_average


class ManagerPage(BasePage):
    """Page object for manager functionality"""

    URL = settings.BASE_URL + settings.BANKING_MANAGER_PATH

    def open(self) -> "ManagerPage":
        self.open_url(self.URL)
        self.wait_for_element(ManagerPageLocators.ADD_CUSTOMER_TAB)
        return self

    # Add customer methods
    @allure.step("Переходим в меню добавление пользователя")
    def go_to_add_customer(self) -> "ManagerPage":
        self.click_element(ManagerPageLocators.ADD_CUSTOMER_TAB)
        return self

    @allure.step("Вводим Имя")
    def enter_first_name(self, first_name: str) -> "ManagerPage":
        self.enter_text(ManagerPageLocators.FIRST_NAME_INPUT, first_name)
        return self

    @allure.step("Вводим фамилию")
    def enter_last_name(self, last_name: str) -> "ManagerPage":
        self.enter_text(ManagerPageLocators.LAST_NAME_INPUT, last_name)
        return self

    @allure.step("Вводим пост код")
    def enter_post_code(self, post_code: str) -> "ManagerPage":
        self.enter_text(ManagerPageLocators.POST_CODE_INPUT, post_code)
        return self

    @allure.step("Нажимаем на кнопку добавить пользователя")
    def click_add_customer(self) -> "ManagerPage":
        self.click_element(ManagerPageLocators.ADD_CUSTOMER_BUTTON)
        return self

    @allure.step("Получаем текст алерта")
    def get_alert_text(self) -> str:
        try:
            alert = self.driver.switch_to.alert
            text = alert.text
            alert.accept()
            return text
        except NoAlertPresentException:
            return ""

    # Customer tab methods
    @allure.step("Переходим в меню с таблицей пользователей")
    def go_to_customers(self):
        self.click_element(ManagerPageLocators.CUSTOMERS_TAB)
        return self

    @allure.step("Получаем список имен пользователей")
    def get_customer_names(self) -> list[str]:
        name_elements = self.find_elements(ManagerPageLocators.FIRST_NAME_CELLS)
        return [element.text for element in name_elements]

    @allure.step("Сортируем пользователей по имени")
    def sort_customers_by_first_name(self, ascending: bool = True) -> "ManagerPage":
        initial_names = self.get_customer_names()

        self.click_element(ManagerPageLocators.FIRST_NAME_HEADER)
        current_names = self.get_customer_names()

        if ascending != (current_names == sorted(initial_names)):
            self.click_element(ManagerPageLocators.FIRST_NAME_HEADER)
            current_names = self.get_customer_names()

        expected_names = sorted(initial_names, reverse=not ascending)
        if current_names != expected_names:
            raise Exception(
                f"Failed to sort customers by first name.\n"
                f"Expected: {expected_names}\n"
                f"Got: {current_names}\n"
                f"Sort direction: {'ascending' if ascending else 'descending'}"
            )

        return self

    @allure.step("Удаляем пользователя с соответсвующим именем")
    def delete_customer_by_name(self, first_name: str):
        rows = self.find_elements(ManagerPageLocators.CUSTOMER_ROWS)
        for i, row in enumerate(rows):
            name_cell = row.find_element("xpath", "./td[1]")
            if name_cell.text == first_name:
                delete_button = row.find_element("xpath", "./td[5]/button")
                delete_button.click()
                break
        return self

    @allure.step("Проверяем существует ли пользователь в таблице")
    def is_customer_present(self, first_name: str) -> bool:
        self.go_to_customers()
        names = self.get_customer_names()
        return first_name in names

    @allure.step("Находим пользователя для удаления по алгоритму")
    def find_customer_to_delete(self) -> str:
        names = self.get_customer_names()
        if not names:
            return ""
        closest_name = find_closest_name_to_average(names)

        return closest_name
