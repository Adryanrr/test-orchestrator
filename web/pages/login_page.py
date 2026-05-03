from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    URL = "https://www.saucedemo.com/"
    _username = (By.ID, "user-name")
    _password = (By.ID, "password")
    _login_btn = (By.ID, "login-button")

    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver
        self._wait = WebDriverWait(driver, 10)

    def open(self) -> None:
        self._driver.get(self.URL)
        self._wait.until(EC.visibility_of_element_located(self._username))

    def fill_credentials(self, username: str, password: str) -> None:
        self._wait.until(EC.visibility_of_element_located(self._username)).send_keys(username)
        self._wait.until(EC.visibility_of_element_located(self._password)).send_keys(password)

    def click_login(self) -> None:
        self._wait.until(EC.element_to_be_clickable(self._login_btn)).click()
        self._wait.until(EC.url_contains("inventory"))
