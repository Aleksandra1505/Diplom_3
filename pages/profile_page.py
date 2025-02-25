from pages.base_page import BasePage
from locators.profile_locators import ProfileLocators
from pages.url import ORDER_HISTORY_URL, LOGIN_PAGE_URL, MAIN_PAGE_URL, PROFILE_URL
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure


class ProfilePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    @allure.step('Ввод эмейла')
    def enter_email_profile(self, email):
        self.find_elements_with_wait(ProfileLocators.EMAIL_INPUT).send_keys(email)

    @allure.step('Ввод пароля')
    def enter_password_profile(self, password):
        self.find_elements_with_wait(ProfileLocators.PASSWORD_INPUT).send_keys(password)


    """Ниже собраны новые методы, созданные в рамках доработок"""
    @allure.step('Авторизация')
    def login_as_default_user(self):
        self.go_to_login_page()
        self.enter_email_profile("antropova2.0@gmail.com")
        self.enter_password_profile("111111")
        self.click_to_element(ProfileLocators.LOGIN_BUTTON)
        WebDriverWait(self.driver, 30).until(EC.url_to_be(MAIN_PAGE_URL))

    @allure.step('Переход в профиль')
    def go_to_profile(self):
        self.click_to_element(ProfileLocators.BUTTON_PROFILE)
        WebDriverWait(self.driver, 10).until(EC.url_to_be(PROFILE_URL))

    @allure.step('Переход в раздел «История заказов»')
    def go_to_order_history(self):
        self.click_to_element(ProfileLocators.ORDER_HISTORY_BUTTON)
        WebDriverWait(self.driver, 10).until(EC.url_to_be(ORDER_HISTORY_URL))

    @allure.step('Выход из аккаунта')
    def logout(self):
        self.click_to_element(ProfileLocators.LOGOUT_BUTTON)
        WebDriverWait(self.driver, 10).until(EC.url_to_be(LOGIN_PAGE_URL))
