from collections.abc import Generator
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

REPORTS_DIR = Path(__file__).resolve().parent.parent / "reports"


@pytest.fixture(scope="function")
def driver(request: pytest.FixtureRequest) -> Generator[webdriver.Chrome, None, None]:
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--window-size=1920,1080")
    chrome_driver = webdriver.Chrome(options=options)
    yield chrome_driver

    rep_call = getattr(request.node, "rep_call", None)
    if rep_call is not None and rep_call.failed:
        REPORTS_DIR.mkdir(parents=True, exist_ok=True)
        screenshot_path = REPORTS_DIR / f"{request.node.name}.png"
        chrome_driver.save_screenshot(str(screenshot_path))
        print(f"\n[screenshot saved] {screenshot_path}")
        print(f"[final url] {chrome_driver.current_url}")

    chrome_driver.quit()


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item: pytest.Item, call: pytest.CallInfo[None]) -> Generator:
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)
