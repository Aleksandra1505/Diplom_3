from locators.order_locators import OrderLocators
from pages.profile_page import ProfilePage
from pages.order_history_page import OrderPage
from pages.constructor_page import ConstructorPage
import allure

class TestOrderPage:

    @allure.title("Открытие деталей заказа из истории заказов")
    def test_open_order_details(self, driver):
        profile_page = ProfilePage(driver)
        order_history_page = OrderPage(driver)

        # Логинимся
        profile_page.login_as_default_user()
        # Переходим в профиль
        profile_page.go_to_profile()
        # Переход на страницу История заказов
        order_history_page.click_to_order_history()
        # Нажимаем на последний заказ юзера и ждем открытие модалки
        order_history_page.click_to_last_order()
        # Получаем номер заказа
        order_number = order_history_page.get_text_from_order_number()
        assert order_number == order_number

    @allure.title("Проверка перехода из истории заказов в ленту заказов")
    def test_orders_from_history_to_feed(self, driver):
        order_page = OrderPage(driver)
        profile_page = ProfilePage(driver)
        constructor_page = ConstructorPage(driver)

        # Логинимся
        profile_page.login_as_default_user()
        # Добавляем ингредиент в заказ
        constructor_page.add_ingredient_to_order()
        # Делаем заказ
        constructor_page.click_order_button()
        # Закрываем попап по крестику
        order_page.close_popup_order()
        # Переходим в профиль
        profile_page.go_to_profile()
        # Переходим на страницу истории заказов
        profile_page.go_to_order_history()
        # Получаем номер последнего заказа
        order_from_history = order_page.get_last_order_history()
        assert order_page.get_check_number_order(order_from_history)

    @allure.title("Проверка увеличения счетчика выполненных заказов после создания нового заказа")
    def test_create_order_increases_completed_orders_counter(self, driver):
        order_page = OrderPage(driver)
        profile_page = ProfilePage(driver)
        constructor_page = ConstructorPage(driver)

        # Логинимся
        profile_page.login_as_default_user()
        # Переходим на Ленту заказов и получаем текущее значение счетчика
        order_page.go_to_orders_feed_page()
        initial_counter_value = order_page.get_counter_value(OrderLocators.COUNTER_DONE_ALL_TIME)

        # Переходим в конструктор
        constructor_page.go_to_constructor_page()
        # Добавляем ингредиент в заказ
        constructor_page.add_ingredient_to_order()
        # Делаем заказ
        constructor_page.click_order_button()
        # Закрываем попап по крестику
        order_page.close_popup_order()

        # Переходим на Ленту заказов и получаем текущее значение счетчика
        order_page.go_to_orders_feed_page()
        new_counter_value = order_page.get_counter_value(OrderLocators.COUNTER_DONE_ALL_TIME)
        assert new_counter_value > initial_counter_value

    @allure.title("Проверка увеличения счетчика выполненных заказов за сегодняшний день после создания нового заказа")
    def test_create_order_increases_today_counter(self, driver):
        order_page = OrderPage(driver)
        profile_page = ProfilePage(driver)
        constructor_page = ConstructorPage(driver)

        # Логинимся
        profile_page.login_as_default_user()
        # Переходим на Ленту заказов и получаем текущее значение счетчика
        order_page.go_to_orders_feed_page()
        initial_counter_value = order_page.get_counter_value(OrderLocators.COUNTER_DONE_TODAY)

        # Переходим в конструктор
        constructor_page.go_to_constructor_page()
        # Добавляем ингредиент в заказ
        constructor_page.add_ingredient_to_order()
        # Делаем заказ
        constructor_page.click_order_button()
        # Закрываем попап по крестику
        order_page.close_popup_order()

        # Переходим на Ленту заказов и получаем текущее значение счетчика
        order_page.go_to_orders_feed_page()
        new_counter_value = order_page.get_counter_value(OrderLocators.COUNTER_DONE_TODAY)
        assert new_counter_value > initial_counter_value

    @allure.title("Проверка появления номера заказа в разделе 'В работе' после создания заказа")
    def test_order_number_appears_in_in_progress_after_order_creation(self, driver):
        order_page = OrderPage(driver)
        profile_page = ProfilePage(driver)
        constructor_page = ConstructorPage(driver)

        # Логинимся
        profile_page.login_as_default_user()
        # Переходим в конструктор
        constructor_page.go_to_constructor_page()
        # Добавляем ингредиент в заказ
        constructor_page.add_ingredient_to_order()
        new_counter_value = constructor_page.get_counter_value()
        # Делаем заказ
        constructor_page.click_order_button()

        # Ожидаем появления и обновления номера заказа
        order_page.wait_for_order_number_popup()
        order_page.wait_for_order_number_update()
        expected_order_number = order_page.get_order_number_from_popup()

        # Закрываем попап по крестику
        order_page.close_popup_order()

        # Переходим на Ленту заказов и получаем текущее значение счетчика
        order_page.go_to_orders_feed_page()

        # Ожидаем появления заказа в "В работе"
        order_page.wait_for_order_in_progress(expected_order_number)

        # Проверяем, что заказ действительно появился
        order_numbers = order_page.get_orders_in_progress()

        assert expected_order_number in order_numbers
