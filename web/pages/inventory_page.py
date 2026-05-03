from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class InventoryPage:
    _add_to_cart_btn = (By.CSS_SELECTOR, ".inventory_item button")
    _cart_link = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver

    def add_first_item_to_cart(self) -> None:
        self._driver.find_elements(*self._add_to_cart_btn)[0].click()

    def go_to_cart(self) -> None:
        self._driver.find_element(*self._cart_link).click()
