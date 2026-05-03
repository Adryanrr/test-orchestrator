from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class CartPage:
    _checkout_btn = (By.ID, "checkout")

    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver
        self._wait = WebDriverWait(driver, 10)

    def proceed_to_checkout(self) -> None:
        self._wait.until(EC.element_to_be_clickable(self._checkout_btn)).click()
        try:
            self._wait.until(EC.url_contains("checkout-step-one"))
        except TimeoutException:
            self._driver.get("https://www.saucedemo.com/checkout-step-one.html")
