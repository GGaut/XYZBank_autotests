import allure

from pages.manager_page import ManagerPage


class TestDeleteCustomer:
    @allure.title("Удаление клиента")
    def test_delete_customer_closest_to_average_length(
        self, manager_page: ManagerPage, create_test_customers
    ):
        """
        Test Case 3: Deleting a client with the name closest to the average length
        - Get a list of customer names
        - Calculating the length of names
        - Delete the client with the name closest to the average value and check the result
        """

        manager_page.go_to_customers()
        customer_to_delete = manager_page.find_customer_to_delete()
        assert customer_to_delete != "", "Couldn't identify the customer to delete"

        manager_page.delete_customer_by_name(customer_to_delete)

        assert manager_page.is_customer_present(customer_to_delete), (
            f"Customer {customer_to_delete} still in the table"
        )
