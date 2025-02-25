import pytest
from selenium import webdriver

@pytest.fixture(params=["chrome", "firefox"])
def driver(request):
    if request.param == "chrome":
        driver = webdriver.Chrome()
    else:
        driver = webdriver.Firefox()

    driver.maximize_window()
    yield driver
    driver.quit()
