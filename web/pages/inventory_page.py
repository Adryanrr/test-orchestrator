from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class InventoryPage:
    _inventory_container = (By.CLASS_NAME, "inventory_list")
    _add_to_cart_btn = (By.CSS_SELECTOR, "button[id^='add-to-cart']")
    _cart_badge = (By.CLASS_NAME, "shopping_cart_badge")
    _cart_link = (By.CLASS_NAME, "shopping_cart_link")

    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver
        self._wait = WebDriverWait(driver, 10)

    def add_first_item_to_cart(self) -> None:
        self._wait.until(EC.visibility_of_element_located(self._inventory_container))
        buttons = self._wait.until(
            EC.presence_of_all_elements_located(self._add_to_cart_btn)
        )
        buttons[0].click()
        self._wait.until(EC.visibility_of_element_located(self._cart_badge))

    def go_to_cart(self) -> None:
        cart_link = self._wait.until(EC.element_to_be_clickable(self._cart_link))
        self._driver.execute_script("arguments[0].scrollIntoView(true);", cart_link)
        cart_link.click()
        self._wait.until(EC.url_contains("/cart.html"))
