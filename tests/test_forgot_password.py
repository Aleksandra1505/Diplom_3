from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.forgot_password_page import ForgotPasswordPageMetood
from locators.forgot_password_locators import ForgotPasswordLocators
from pages.url import RESET_PASSWORD_URL
import allure

class TestForgotPassword:

    @allure.title("Переход на страницу восстановления пароля")
    def test_go_to_forgot_password_page(self, driver):
        forgot_password_page = ForgotPasswordPageMetood(driver)
        forgot_password_page.go_to_forgot_password_page()
        assert forgot_password_page.is_element_visible(ForgotPasswordLocators.PASSWORD_RECOVERY_HEADER)

    @allure.title("ввод почты и клик по кнопке «Восстановить»")
    def test_reset_password(self, driver):
        email = "sasha-antropova@yandex.ru"
        forgot_password_page = ForgotPasswordPageMetood(driver)
        forgot_password_page.go_to_forgot_password_page()

        forgot_password_page.enter_email(email)
        forgot_password_page.click_restore_password_button()

        WebDriverWait(driver, 10).until(EC.url_to_be(RESET_PASSWORD_URL))

        assert forgot_password_page.find_elements_with_wait(ForgotPasswordLocators.PASSWORD_LABEL).is_displayed()

    @allure.title("клик по кнопке показать/скрыть пароль делает поле активным — подсвечивает его")
    def test_toggle_show_password(self, driver):
        password = "111111"
        login_page = ForgotPasswordPageMetood(driver)
        login_page.go_to_login_page()

        login_page.enter_password(password)
        login_page.toggle_show_password()

        assert login_page.get_password_input_type() == "text"