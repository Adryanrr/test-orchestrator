from web.pages.login_page import LoginPage
from web.pages.inventory_page import InventoryPage
from web.pages.cart_page import CartPage
from web.pages.checkout_page import CheckoutPage


def test_complete_purchase_flow(driver):
    login = LoginPage(driver)
    login.open()
    login.fill_credentials("standard_user", "secret_sauce")
    login.click_login()

    inventory = InventoryPage(driver)
    inventory.add_first_item_to_cart()
    inventory.go_to_cart()

    cart = CartPage(driver)
    cart.proceed_to_checkout()

    checkout = CheckoutPage(driver)
    checkout.fill_info("Test", "User", "12345")
    checkout.finish()

    assert checkout.get_confirmation_message() == "Thank you for your order!"


def test_login_invalid_credentials(driver) -> None:
    login = LoginPage(driver)
    login.open()
    login.fill_credentials("standard_user", "wrong_password")
    login.attempt_login()
    assert "Username and password do not match" in login.get_error_message()


def test_login_locked_user(driver) -> None:
    login = LoginPage(driver)
    login.open()
    login.fill_credentials("locked_out_user", "secret_sauce")
    login.attempt_login()
    assert "locked out" in login.get_error_message()
