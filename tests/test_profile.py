import allure
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.profile_page import ProfilePage
from locators.profile_locators import ProfileLocators
from pages.url import PROFILE_URL, MAIN_PAGE_URL, ORDER_HISTORY_URL, LOGIN_PAGE_URL


class TestProfile:
    @allure.title("Переход на страницу профиля после авторизации")
    def test_go_to_profile(self, driver):
        profile_page = ProfilePage(driver)

        profile_page.go_to_login_page()
        profile_page.click_to_element(ProfileLocators.BUTTON_PROFILE)

        profile_page.enter_email_profile("antropova2.0@gmail.com")
        profile_page.enter_password_profile("111111")
        profile_page.click_to_element(ProfileLocators.LOGIN_BUTTON)

        WebDriverWait(driver, 10).until(EC.url_to_be(MAIN_PAGE_URL))

        profile_page.click_to_element(ProfileLocators.BUTTON_PROFILE)

        WebDriverWait(driver, 10).until(EC.url_to_be(PROFILE_URL))

        assert driver.current_url == PROFILE_URL

    @allure.title("Переход на страницу истории заказов после авторизации")
    def test_go_to_order_history(self, driver):
        profile_page = ProfilePage(driver)

        profile_page.go_to_login_page()
        profile_page.click_to_element(ProfileLocators.BUTTON_PROFILE)

        profile_page.enter_email_profile("antropova2.0@gmail.com")
        profile_page.enter_password_profile("111111")
        profile_page.click_to_element(ProfileLocators.LOGIN_BUTTON)
        WebDriverWait(driver, 10).until(EC.url_to_be(MAIN_PAGE_URL))

        profile_page.click_to_element(ProfileLocators.BUTTON_PROFILE)
        WebDriverWait(driver, 10).until(EC.url_to_be(PROFILE_URL))

        profile_page.click_to_element(ProfileLocators.ORDER_HISTORY_BUTTON)
        WebDriverWait(driver, 10).until(EC.url_to_be(ORDER_HISTORY_URL))

        assert driver.current_url == ORDER_HISTORY_URL

    @allure.title("Выход из аккаунта и переход на страницу входа")
    def test_exit_from_account(self, driver):
        profile_page = ProfilePage(driver)

        profile_page.go_to_login_page()
        profile_page.click_to_element(ProfileLocators.BUTTON_PROFILE)

        profile_page.enter_email_profile("antropova2.0@gmail.com")
        profile_page.enter_password_profile("111111")
        profile_page.click_to_element(ProfileLocators.LOGIN_BUTTON)
        WebDriverWait(driver, 10).until(EC.url_to_be(MAIN_PAGE_URL))

        profile_page.click_to_element(ProfileLocators.BUTTON_PROFILE)
        WebDriverWait(driver, 10).until(EC.url_to_be(PROFILE_URL))

        profile_page.click_to_element(ProfileLocators.LOGOUT_BUTTON)
        WebDriverWait(driver, 10).until(EC.url_to_be(LOGIN_PAGE_URL))

        assert driver.current_url == LOGIN_PAGE_URL