from selenium.webdriver.common.by import By


class ManagerPageLocators:
    """Locators for Manager page elements"""

    # Navigation Tabs
    ADD_CUSTOMER_TAB = (By.CSS_SELECTOR, "button[ng-click*='addCust']")
    CUSTOMERS_TAB = (By.CSS_SELECTOR, "button[ng-click*='showCust']")

    # Add Customer Form
    FIRST_NAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='First Name']")
    LAST_NAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Last Name']")
    POST_CODE_INPUT = (By.CSS_SELECTOR, "input[placeholder='Post Code']")
    ADD_CUSTOMER_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")

    # Customers Table
    CUSTOMERS_TABLE = (By.CSS_SELECTOR, "table.table-bordered")
    FIRST_NAME_HEADER = (By.CSS_SELECTOR, "a[ng-click*=\"sortType = 'fName'\"]")
    DELETE_BUTTON = (By.CSS_SELECTOR, "button[ng-click*='deleteCust']")

    # Table structure
    CUSTOMER_ROWS = (By.CSS_SELECTOR, "table.table-bordered tbody tr")
    FIRST_NAME_CELLS = (By.CSS_SELECTOR, "table.table-bordered tbody tr td:first-child")
