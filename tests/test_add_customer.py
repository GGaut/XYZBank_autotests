import allure

from pages.manager_page import ManagerPage
from utils.data_generator import (
    generate_last_name,
    generate_post_code,
    post_code_to_name,
)


class TestAddCustomer:
    @allure.title("Добавление клиента")
    @allure.description("""
        Test case 1: Creating a client with automatically generated data
         - Generating a 10-digit Post Code
         - Convert the Post Code to the First Name using the algorithm
         - Adding a client
         - Checking the successful addition
        """)
    def test_add_customer_with_generated_data(self, manager_page: ManagerPage):
        post_code = generate_post_code()
        first_name = post_code_to_name(post_code)
        last_name = generate_last_name()

        (
            manager_page.go_to_add_customer()
            .enter_first_name(first_name)
            .enter_last_name(last_name)
            
            .enter_post_code(post_code)
            .click_add_customer()
        )

        alert_text = manager_page.get_alert_text()
        assert (
            "Customer added successfully" in alert_text
            or "success" in alert_text.lower()
        )

        assert manager_page.is_customer_present(first_name), (
            f"Customer {first_name} is not in the table"
        )
