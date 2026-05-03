from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver


class LoginPage:
    URL = "https://www.saucedemo.com/"
    _username = (By.ID, "user-name")
    _password = (By.ID, "password")
    _login_btn = (By.ID, "login-button")

    def __init__(self, driver: WebDriver) -> None:
        self._driver = driver

    def open(self) -> None:
        self._driver.get(self.URL)

    def fill_credentials(self, username: str, password: str) -> None:
        self._driver.find_element(*self._username).send_keys(username)
        self._driver.find_element(*self._password).send_keys(password)

    def click_login(self) -> None:
        self._driver.find_element(*self._login_btn).click()
