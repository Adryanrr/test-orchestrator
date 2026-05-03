from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class InventoryPage:
    _add_to_cart_btn = (By.CSS_SELECTOR, ".inventory_item button")
    _cart_link = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver
        self._wait = WebDriverWait(driver, 10)

    def add_first_item_to_cart(self) -> None:
        self._wait.until(EC.element_to_be_clickable(self._add_to_cart_btn)).click()

    def go_to_cart(self) -> None:
        self._wait.until(EC.element_to_be_clickable(self._cart_link)).click()
