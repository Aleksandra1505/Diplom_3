import allure
from pages.profile_page import ProfilePage
from pages.url import PROFILE_URL, ORDER_HISTORY_URL, LOGIN_PAGE_URL

class TestProfile:
    @allure.title("Переход на страницу профиля после авторизации")
    def test_go_to_profile(self, driver):
        profile_page = ProfilePage(driver)
        # Логинимся
        profile_page.login_as_default_user()
        # Переходим в профиль
        profile_page.go_to_profile()
        assert driver.current_url == PROFILE_URL

    @allure.title("Переход на страницу истории заказов после авторизации")
    def test_go_to_order_history(self, driver):
        profile_page = ProfilePage(driver)
        # Логинимся
        profile_page.login_as_default_user()
        # Переходим в профиль
        profile_page.go_to_profile()
        # Переходим на страницу истории заказов
        profile_page.go_to_order_history()
        assert driver.current_url == ORDER_HISTORY_URL

    @allure.title("Выход из аккаунта и переход на страницу входа")
    def test_exit_from_account(self, driver):
        profile_page = ProfilePage(driver)
        # Логинимся
        profile_page.login_as_default_user()
        # Переходим в профиль
        profile_page.go_to_profile()
        # Выходим из личного кабинета
        profile_page.logout()
        assert driver.current_url == LOGIN_PAGE_URL