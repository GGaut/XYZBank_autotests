class Settings:
    BASE_URL: str = "https://www.globalsqa.com"

    BANKING_MANAGER_PATH: str = "/angularJs-protractor/BankingProject/#/manager"

    HEADLESS: bool = True
    WINDOW_WIDTH: int = 1920
    WINDOW_HEIGHT: int = 1080

    WAIT_TIMER: int = 20

    ALLURE_RESULTS_DIR: str = "./allure-results"


settings = Settings()
