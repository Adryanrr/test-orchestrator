from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

JS_SET_INPUT = """
var nativeSetter = Object.getOwnPropertyDescriptor(
    window.HTMLInputElement.prototype, 'value').set;
nativeSetter.call(arguments[0], arguments[1]);
arguments[0].dispatchEvent(new Event('input', { bubbles: true }));
arguments[0].dispatchEvent(new Event('change', { bubbles: true }));
"""


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

    def _set_input(self, locator: tuple, value: str) -> None:
        element = self._wait.until(EC.visibility_of_element_located(locator))
        self._driver.execute_script(JS_SET_INPUT, element, value)

    def _js_click(self, locator: tuple) -> None:
        element = self._wait.until(EC.element_to_be_clickable(locator))
        self._driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
        self._driver.execute_script("arguments[0].click();", element)

    def fill_info(self, first_name: str, last_name: str, zip_code: str) -> None:
        self._set_input(self._first_name, first_name)
        self._set_input(self._last_name, last_name)
        self._set_input(self._zip_code, zip_code)
        self._js_click(self._continue_btn)
        self._wait.until(EC.url_contains("checkout-step-two.html"))

    def finish(self) -> None:
        self._js_click(self._finish_btn)
        self._wait.until(EC.url_contains("checkout-complete.html"))

    def get_confirmation_message(self) -> str:
        return self._wait.until(EC.visibility_of_element_located(self._confirmation)).text
