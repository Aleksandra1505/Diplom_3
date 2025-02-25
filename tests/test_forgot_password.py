from pages.forgot_password_page import ForgotPasswordPage
from locators.forgot_password_locators import ForgotPasswordLocators
import allure

class TestForgotPassword:

    @allure.title("Переход на страницу восстановления пароля")
    def test_go_to_forgot_password_page(self, driver):
        forgot_password_page = ForgotPasswordPage(driver)
        # Переход на страницу восстановления пароля
        forgot_password_page.go_to_forgot_password_page()
        assert forgot_password_page.is_element_visible(ForgotPasswordLocators.PASSWORD_RECOVERY_HEADER)

    @allure.title("Ввод почты и клик по кнопке «Восстановить»")
    def test_reset_password(self, driver):
        forgot_password_page = ForgotPasswordPage(driver)
        # Переход на страницу восстановления пароля
        forgot_password_page.go_to_forgot_password_page()
        # Ввод эмейла в поле ввода
        forgot_password_page.enter_email()
        # Нажатие на кнопку восстановить пароль
        forgot_password_page.click_restore_password_button()
        assert forgot_password_page.find_elements_with_wait(ForgotPasswordLocators.PASSWORD_LABEL).is_displayed()

    @allure.title("Клик по кнопке показать/скрыть пароль делает поле активным — подсвечивает его")
    def test_toggle_show_password(self, driver):
        login_page = ForgotPasswordPage(driver)
        # Переход на страницу логина
        login_page.go_to_login_page()
        # Ввод пароля в поле пароль
        login_page.enter_password()
        # Нажать на кнопку показа пароля
        login_page.toggle_show_password()
        assert login_page.get_password_input_type() == "text"