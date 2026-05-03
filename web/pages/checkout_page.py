from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains


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
        fn = self._wait.until(EC.visibility_of_element_located(self._first_name))
        ActionChains(self._driver).move_to_element(fn).click().send_keys(first_name).perform()
        
        ln = self._wait.until(EC.visibility_of_element_located(self._last_name))
        ActionChains(self._driver).move_to_element(ln).click().send_keys(last_name).perform()
        
        zp = self._wait.until(EC.visibility_of_element_located(self._zip_code))
        ActionChains(self._driver).move_to_element(zp).click().send_keys(zip_code).perform()
        
        cont = self._wait.until(EC.element_to_be_clickable(self._continue_btn))
        self._driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", cont)
        ActionChains(self._driver).move_to_element(cont).click().perform()
        self._wait.until(EC.url_contains("checkout-step-two.html"))

    def finish(self) -> None:
        btn = self._wait.until(EC.element_to_be_clickable(self._finish_btn))
        self._driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        btn.click()
        self._wait.until(EC.url_contains("checkout-complete.html"))

    def get_confirmation_message(self) -> str:
        return self._wait.until(EC.visibility_of_element_located(self._confirmation)).text
