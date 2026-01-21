import allure

from pages.manager_page import ManagerPage


class TestSortCustomers:
    @allure.title("Сортировка клиентов по имени")
    @allure.description("""
        Test Case 2: Sorting customers by name
        - Get initial list of unsorted customer names
        - Click sort for ascending order, verify A->Z sorting
        - Click sort again for descending order, verify Z->A sorting
        - Verify we can return to ascending order
        """)
    def test_sort_customers_by_first_name_asc_desc(
        self, manager_page: ManagerPage, create_test_customers
    ):
        manager_page.go_to_customers()
        initial_names = manager_page.get_customer_names()

        manager_page.sort_customers_by_first_name(ascending=True)
        asc_names = manager_page.get_customer_names()
        assert asc_names == sorted(initial_names), (
            "Names not in ascending order (A->Z)\n"
            f"Expected: {sorted(initial_names)}\n"
            f"Got: {asc_names}"
        )

        manager_page.sort_customers_by_first_name(ascending=False)
        desc_names = manager_page.get_customer_names()
        assert desc_names == sorted(initial_names, reverse=True), (
            "Names not in descending order (Z->A)\n"
            f"Expected: {sorted(initial_names, reverse=True)}\n"
            f"Got: {desc_names}"
        )

        manager_page.sort_customers_by_first_name(ascending=True)
        final_names = manager_page.get_customer_names()
        assert final_names == asc_names, (
            "Names did not return to ascending order\n"
            f"Expected: {asc_names}\n"
            f"Got: {final_names}"
        )
