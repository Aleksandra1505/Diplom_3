from pages.constructor_page import ConstructorPage
from locators.constructor_locators import ConstructorLocators
from pages.profile_page import ProfilePage
from pages.url import MAIN_PAGE_URL, FEED_URL
import allure

class TestConstructor:
    @allure.title("Переход на страницу конструктора")
    def test_go_to_constructor(self, driver):
        constructor_page = ConstructorPage(driver)
        # Открываем главную страницу
        constructor_page.open_main_page()
        # Переходим в конструктор
        constructor_page.go_to_constructor_page()
        assert driver.current_url == MAIN_PAGE_URL

    @allure.title("Переход на Ленту заказов")
    def test_go_to_orders_feed(self, driver):
        constructor_page = ConstructorPage(driver)
        # Открываем главную страницу
        constructor_page.open_main_page()
        # Переходим на Ленту заказов
        constructor_page.go_to_orders_feed_page()
        assert driver.current_url == FEED_URL

    @allure.title("Открытие попапа с информацией об ингредиенте")
    def test_ingredient_info_popup(self, driver):
        constructor_page = ConstructorPage(driver)
        # Открываем главную страницу
        constructor_page.open_main_page()
        # Нажимаем на ингредиент и дожидаемся появления попапа
        constructor_page.open_ingredient_info()
        assert constructor_page.is_element_visible(ConstructorLocators.INFO_INGREDIENT)

    @allure.title("Закрытие попапа с информацией об ингредиенте по клику на крестик")
    def test_close_ingredient_info_popup_by_clicking_cross(self, driver):
        constructor_page = ConstructorPage(driver)
        # Открываем главную страницу
        constructor_page.open_main_page()
        # Нажимаем на ингредиент и дожидаемся появления попапа
        constructor_page.open_ingredient_info()
        # Закрываем попап по крестику
        constructor_page.close_ingredient_info()
        assert constructor_page.is_element_not_visible(ConstructorLocators.INFO_INGREDIENT)

    @allure.title("Добавление ингредиента в заказ увеличивает счетчик")
    def test_add_ingredient_to_order(self, driver):
        constructor_page = ConstructorPage(driver)
        # Открываем главную страницу
        constructor_page.open_main_page()
        # Получаем начальное значение счетчика
        initial_counter_value = constructor_page.get_initial_counter_value()
        # Добавляем ингредиент в заказ
        constructor_page.add_ingredient_to_order()
        # Получаем новое значение счетчика
        new_counter_value = constructor_page.get_new_counter_value()
        assert new_counter_value > initial_counter_value

    @allure.title("Добавление ингредиента в заказ и оформление заказа с подтверждением")
    def test_add_order(self, driver):
        profile_page = ProfilePage(driver)
        constructor_page = ConstructorPage(driver)
        # Логинимся
        profile_page.login_as_default_user()
        # Добавляем ингредиент в заказ
        constructor_page.add_ingredient_to_order()
        # Делаем заказ
        constructor_page.click_order_button()
        assert constructor_page.is_order_confirmation_displayed()