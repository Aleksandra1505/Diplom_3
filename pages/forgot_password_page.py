from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePageMetod
from locators.forgot_password_locators import ForgotPasswordLocators
from pages.url import LOGIN_PAGE_URL
import allure

class ForgotPasswordPageMetood(BasePageMetod):
    def __init__(self, driver):
        self.driver = driver

    @allure.step('Перейти на страницу восстановления пароля')
    def go_to_forgot_password_page(self):
        self.driver.get(LOGIN_PAGE_URL)
        # Ожидание кликабельности ссылки и прокрутка в область видимости
        forgot_password_link = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable(ForgotPasswordLocators.FORGOT_PASSWORD_LINK))
        # Кликаем по элементу
        forgot_password_link.click()

    @allure.step("Переход на страницу логина")
    def go_to_login_page(self):
        self.driver.get(LOGIN_PAGE_URL)

    @allure.step('Ввод эмейла')
    def enter_email(self, email):
        self.find_elements_with_wait(ForgotPasswordLocators.EMAIL_INPUT).send_keys(email)

    @allure.step('Ввод пароля')
    def enter_password(self, password):
        self.find_elements_with_wait(ForgotPasswordLocators.PASSWORD_LABEL).send_keys(password)

    @allure.step('Клик по кнопке Восстановить')
    def click_restore_password_button(self):
        self.click_to_element(ForgotPasswordLocators.RECOVER_BUTTON)

    @allure.step('Клик по кнопке скрытия элемента')
    def toggle_show_password(self):
        self.click_to_element(ForgotPasswordLocators.SHOW_PASSWORD)

    def get_password_input_type(self):
        return self.find_elements_with_wait(ForgotPasswordLocators.PASSWORD_LABEL).get_attribute("type")