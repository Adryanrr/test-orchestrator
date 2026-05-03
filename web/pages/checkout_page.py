from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CheckoutPage:
    _first_name = (By.ID, "first-name")
    _last_name = (By.ID, "last-name")
    _zip_code = (By.ID, "postal-code")
    _continue_btn = (By.ID, "continue")
    _finish_btn = (By.ID, "finish")
    _confirmation = (By.CLASS_NAME, "complete-header")

    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver
        self._wait = WebDriverWait(driver, 10)

    def fill_info(self, first_name: str, last_name: str, zip_code: str) -> None:
        fn = self._wait.until(EC.element_to_be_clickable(self._first_name))
        fn.click()
        fn.send_keys(first_name)
        self._driver.find_element(*self._last_name).send_keys(last_name)
        self._driver.find_element(*self._zip_code).send_keys(zip_code)
        self._driver.find_element(*self._continue_btn).click()

    def finish(self) -> None:
        self._driver.find_element(*self._finish_btn).click()

    def get_confirmation_message(self) -> str:
        return self._driver.find_element(*self._confirmation).text
