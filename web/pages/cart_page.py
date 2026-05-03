from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class CartPage:
    _checkout_btn = (By.ID, "checkout")

    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver

    def proceed_to_checkout(self) -> None:
        self._driver.find_element(*self._checkout_btn).click()
