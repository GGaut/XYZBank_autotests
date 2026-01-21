import os

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from config.settings import settings
from pages.manager_page import ManagerPage
from utils.data_generator import (
    generate_first_name,
    generate_last_name,
    generate_post_code,
)


@pytest.fixture()
def driver(request):
    """A fixture for initializing the WebDriver"""
    selenoid_url = os.environ.get("SELENOID_URL")

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument(
        f"--window-size={settings.WINDOW_WIDTH},{settings.WINDOW_HEIGHT}"
    )

    if selenoid_url:
        capabilities = {
            "browserName": "chrome",
            "browserVersion": "120.0",
            "selenoid:options": {"enableVNC": True, "enableVideo": False},
        }
        chrome_options.set_capability(
            "selenoid:options", capabilities["selenoid:options"]
        )
        driver = webdriver.Remote(command_executor=selenoid_url, options=chrome_options)

    else:
        if settings.HEADLESS:
            chrome_options.add_argument("--headless")

        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
    request.node.driver = driver
    yield driver
    driver.quit()


@pytest.fixture()
def manager_page(driver):
    """A fixture for initializing the manager page"""
    page = ManagerPage(driver)
    page.open()
    return page


@pytest.fixture()
def create_test_customers(driver):
    """
    A fixture for creating test customers
    """
    page = ManagerPage(driver)
    created_customers = []

    with allure.step("Создание трех тестовых клиентов"):
        for _ in range(3):
            post_code = generate_post_code()
            first_name = generate_first_name()
            last_name = generate_last_name()

            page.go_to_add_customer().enter_first_name(first_name).enter_last_name(
                last_name
            ).enter_post_code(post_code).click_add_customer()
            alert = driver.switch_to.alert
            alert.accept()
            created_customers.append(
                {
                    "first_name": first_name,
                    "last_name": last_name,
                    "post_code": post_code,
                }
            )

    yield created_customers

    with allure.step("Удаление тестовых клиентов"):
        for customer in created_customers:
            page.delete_customer_by_name(customer["first_name"])


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """A hook for tracking test crashes and creating screenshots for Allure"""
    outcome = yield
    rep = outcome.get_result()

    if rep.failed and rep.when == "call":
        driver = getattr(item._request.node, "_driver", None)
        if driver:
            allure.attach(
                driver.get_screenshot_as_png(),
                name="failure_screenshot",
                attachment_type=allure.attachment_type.PNG,
            )
