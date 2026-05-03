from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CartPage:
    _cart_list = (By.CLASS_NAME, "cart_list")
    _cart_item = (By.CLASS_NAME, "cart_item")
    _checkout_btn = (By.ID, "checkout")

    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver
        self._wait = WebDriverWait(driver, 10)

    def proceed_to_checkout(self) -> None:
        self._wait.until(EC.visibility_of_element_located(self._cart_list))
        self._wait.until(EC.visibility_of_element_located(self._cart_item))
        btn = self._wait.until(EC.element_to_be_clickable(self._checkout_btn))
        self._driver.execute_script("arguments[0].scrollIntoView(true);", btn)
        btn.click()
        self._wait.until(EC.url_contains("/checkout-step-one.html"))
