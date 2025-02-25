from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
from locators.forgot_password_locators import ForgotPasswordLocators
from pages.url import LOGIN_PAGE_URL, RESET_PASSWORD_URL
import allure

class ForgotPasswordPage(BasePage):
    def __init__(self, driver):
        self.driver = driver

    @allure.step('Перейти на страницу восстановления пароля')
    def go_to_forgot_password_page(self):
        self.driver.get(LOGIN_PAGE_URL)
        # Ожидаем, пока элемент станет доступен для клика
        WebDriverWait(self.driver, 20).until(
            EC.element_to_be_clickable(ForgotPasswordLocators.FORGOT_PASSWORD_LINK)
        )
        self.click_to_element(ForgotPasswordLocators.FORGOT_PASSWORD_LINK)

    @allure.step('Клик по кнопке скрытия элемента')
    def toggle_show_password(self):
        self.click_to_element(ForgotPasswordLocators.SHOW_PASSWORD)

    def get_password_input_type(self):
        return self.find_elements_with_wait(ForgotPasswordLocators.PASSWORD_LABEL).get_attribute("type")

    """Ниже собраны новые методы, созданные в рамках доработок"""
    @allure.step('Ввод эмейла')
    def enter_email(self):
        email = "sasha-antropova@yandex.ru"
        self.find_elements_with_wait(ForgotPasswordLocators.EMAIL_INPUT).send_keys(email)

    @allure.step('Ввод пароля')
    def enter_password(self):
        password = "111111"
        self.find_elements_with_wait(ForgotPasswordLocators.PASSWORD_LABEL).send_keys(password)

    @allure.step('Клик по кнопке Восстановить')
    def click_restore_password_button(self):
        self.click_to_element(ForgotPasswordLocators.RECOVER_BUTTON)
        WebDriverWait(self.driver, 20).until(EC.url_to_be(RESET_PASSWORD_URL))