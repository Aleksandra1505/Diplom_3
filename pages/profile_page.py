from pages.base_page import BasePageMetod
from locators.profile_locators import ProfileLocators
from pages.url import ORDER_HISTORY_URL, LOGIN_PAGE_URL
import allure


class ProfilePage(BasePageMetod):
    def __init__(self, driver):
        super().__init__(driver)

    @allure.step('Перейти на страницу авторизации')
    def go_to_login_page(self):
        self.driver.get(LOGIN_PAGE_URL)

    @allure.step('Ввод эмейла')
    def enter_email_profile(self, email):
        self.find_elements_with_wait(ProfileLocators.EMAIL_INPUT).send_keys(email)

    @allure.step('Ввод пароля')
    def enter_password_profile(self, password):
        self.find_elements_with_wait(ProfileLocators.PASSWORD_INPUT).send_keys(password)


    @allure.step('Переход по клику на «Личный кабинет»')
    def go_to_profile(self):
        self.click_to_element(ProfileLocators.BUTTON_PROFILE)

    @allure.step('Переход в раздел «История заказов»')
    def go_to_order_history(self):
        self.click_to_element(ORDER_HISTORY_URL)

    @allure.step('Выход из аккаунта')
    def logout(self):
        self.click_to_element(ProfileLocators.LOGOUT_BUTTON)